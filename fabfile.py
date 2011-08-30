from fabric.api import env, sudo, cd, run, local, settings as fabric_settings
from fabric.context_managers import prefix
from fabric.contrib import django as fabric_django
from fabric.utils import abort

fabric_django.settings_module('settings')
from django.conf import settings
from south.models import MigrationHistory


__all__= ["staging", "prod", "restart", "restart_apache", "create_database", 
          "load_local_data", "commit_local_data", "commit_prod_data", "migrate",
          "update", "schemamigrate"]

def staging():
    env.hosts = ['root@staging.umeqo.com']
    env.password = settings.STAGING_PASSWORD
    env.directory = '/var/www/umeqo'
    env.activate = 'source /usr/local/pythonenv/UMEQO/bin/activate'

def prod():
    env.hosts = ['root@umeqo.com']
    env.password = settings.PROD_PASSWORD
    env.directory = '/var/www/umeqo'
    env.activate = 'source /usr/local/pythonenv/UMEQO/bin/activate'

def restart_apache():
    if env.host:
        sudo('service apache2 restart')
    else:
        abort("restart cannot be called locally.")
                    
def restart():
    if env.host:
        sudo('service apache2 restart')
        sudo('service nginx restart')
    else:
        abort("restart cannot be called locally.")

def migrate():
    if not env.host:
        with fabric_settings(warn_only=True):
            local("find */migrations -name '*.pyc' | xargs rm")
        local("python manage.py migrate --all")
    else:
        abort("migrate can only be called locally.")
    
def create_database():
    if not env.host:  
        with fabric_settings(warn_only=True):
            local("rm %s" % (settings.DATABASES['default']['NAME']))
        local("python copy_media.py prod in")
        local("python manage.py syncdb --noinput --migrate")
    else:
        with cd(env.directory):
            with prefix(env.activate):
                run('echo "DROP DATABASE umeqo_main; CREATE DATABASE umeqo_main;"|python manage.py dbshell')
                if env.host=="umeqo.com":
                    run("python manage.py syncdb --noinput --migrate")
                else:
                    run("python manage.py syncdb --noinput --migrate")                    
                run("python copy_media.py prod in")
                
def schemamigrate():
    if not env.host:
        apps = list(set(app.app_name for app in MigrationHistory.objects.all()))
        with fabric_settings(warn_only=True):
            for app in apps:
                local("python manage.py schemamigration %s --auto" % app)
    else:
        abort("Schemamigrate can only be called locally.")

def load_local_data():
    if not env.host:
        local("python copy_media.py local in")
        local("python manage.py loaddata ./local_data/fixtures/local_data.json")    
    else:
        if env.host == "umeqo.com":
            abort("load_local_data should not be called on prod.")
        with cd(env.directory):
            with prefix(env.activate):
                run("python copy_media.py local in")
                run("python manage.py loaddata ./local_data/fixtures/local_data.json")  

def commit_prod_data():
    if env.host != "umeqo.com":
        abort("commit_prod_data should only be called on prod")
    with cd(env.directory):
        with prefix(env.activate):
            for app in settings.PROD_DATA_MODELS:
                model_labels = []
                if app == "sites":
                    run("python manage.py dumpdata sites --indent=1 > ./initial_data.json")
                    continue
                fixtures_dir = "./%s/fixtures" % (app)
                with fabric_settings(warn_only=True):
                    run("mkdir %s" % (fixtures_dir))
                for model in settings.PROD_DATA_MODELS[app]:
                    model_labels.append("%s.%s" % (app, model))
                    with fabric_settings(warn_only=True):
                        run("python manage.py file_cleanup %s.%s" % (app, model))
                run("python manage.py dumpdata %s --indent=1 > %s/initial_data.json" % (" ".join(model_labels), fixtures_dir))
            run("python copy_media.py prod out")
            run("git add -A")
            with fabric_settings(warn_only=True):
                run('git commit -m "Prod data commit from prod."')
                run("git push origin master")

def commit_local_data():
    if env.host != "staging.umeqo.com":
        abort("commit_local_data should only be called on staging")
    with cd(env.directory):
        with prefix(env.activate):
            model_labels = []
            for app in settings.LOCAL_DATA_MODELS:
                for model in settings.LOCAL_DATA_MODELS[app]:
                    model_labels.append("%s.%s" % ( app, model))
                    with fabric_settings(warn_only=True):
                        run("python manage.py file_cleanup %s.%s" % (app, model))
            run("python copy_media.py local out")
            with fabric_settings(warn_only=True):
                run("mkdir ./local_data/fixtures")
            run("python manage.py dumpdata %s --indent=1 > ./local_data/fixtures/local_data.json" % (" ".join(model_labels)))
            run("git add -A")
            with fabric_settings(warn_only=True):
                run('git commit -m "Local data commit from staging."')
                run("git push origin dev")

def update():
    if not env.host:
        abort("update can only be called on staging and prod.")
    else:
        with cd(env.directory):
            with prefix(env.activate):
                if env.host=="staging.umeqo.com":
                    commit_local_data()
                    run("git pull origin dev")
                elif env.host=="umeqo.com":
                    commit_prod_data()
                    run("git pull origin prod")
                run("python manage.py migrate --all")
                run("echo 'yes'|python manage.py collectstatic")
                run("chmod 777 logs/ -R")
                run("chmod 777 media/ -R")
                with fabric_settings(warn_only=True):
                    result = run("python manage.py test --setting=settings_test")
                if result.failed:
                    run("git reset --hard master@{1}")
                    run("python manage.py migrate --all")
                    run("echo 'yes'|python manage.py collectstatic")
                restart_apache()