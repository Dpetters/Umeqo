from fabric.api import env, sudo, cd, run, local, settings as fabric_settings
from fabric.context_managers import prefix
from fabric.contrib import django as fabric_django
from fabric.utils import abort

fabric_django.settings_module('settings')
from django.conf import settings
from south.models import MigrationHistory

__all__= ["demo", "staging", "prod", "restart", "restart_apache", "create_database", "load_prod_data",
          "load_local_data", "commit_local_data", "commit_prod_data", "migrate",
          "update", "schemamigrate"]

def demo():
    env.type = "demo"
    env.hosts = ['root@staging.umeqo.com']
    env.password = settings.STAGING_PASSWORD
    env.directory = '/var/www/umeqo_demo'
    env.activate = 'source /usr/local/pythonenv/UMEQO/bin/activate'

def staging():
    env.type = "staging"
    env.hosts = ['root@staging.umeqo.com']
    env.password = settings.STAGING_PASSWORD
    env.directory = '/var/www/umeqo'
    env.activate = 'source /usr/local/pythonenv/UMEQO/bin/activate'

def prod():
    env.type = "prod"
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
                if env.type=="staging":
                    run('echo "DROP DATABASE umeqo_main; CREATE DATABASE umeqo_main;"|python manage.py dbshell')
                elif env.type=="demo":
                    run('echo "DROP DATABASE umeqo_demo_main; CREATE DATABASE umeqo_demo_main;"|python manage.py dbshell')
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
        if env.type == "prod":
            abort("load_local_data should not be called on prod.")
        with cd(env.directory):
            print env.directory
            with prefix(env.activate):
                run("python copy_media.py local in")
                run("python manage.py loaddata ./local_data/fixtures/local_data.json")  

def commit_prod_data():
    if not env.host or env.type != "prod":
        abort("commit_prod_data should only be called on prod")
    with cd(env.directory):
        with prefix(env.activate):
            run("python manage.py dumpdata sites auth.group --indent=1 > ./initial_data.json")
            directories = ""
            for app in settings.PROD_DATA_MODELS:
                model_labels = []
                if app == "sites" or app == "auth":
                    continue
                fixtures_dir = "./%s/fixtures" % (app)
                directories += "%s/* " % fixtures_dir
                with fabric_settings(warn_only=True):
                    run("mkdir %s" % (fixtures_dir))
                for model in settings.PROD_DATA_MODELS[app]:
                    model_labels.append("%s.%s" % (app, model))
                    with fabric_settings(warn_only=True):
                        run("python manage.py file_cleanup %s.%s" % (app, model))
                run("python manage.py dumpdata %s --indent=1 > %s/initial_data.json" % (" ".join(model_labels), fixtures_dir))
            run("python copy_media.py prod out")
            run("git add ./initial_data.json ./prod_data/* %s" % directories)
            with fabric_settings(warn_only=True):
                run('git commit -m "Prod data commit from prod."')
                run("git push origin master")

def load_prod_data():
    if not env.host:
        local("python copy_media.py prod in")
        local("python manage.py flush --noinput")
    else:
        if env.type == "umeqo":
            abort("load_prod_data cannot be called on prod.")
        with cd(env.directory):
            with prefix(env.activate):
                run("python copy_media.py prod in")
                run("python manage.py flush --noinput") 
                
def commit_local_data():
    if env.type != "staging":
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
            run("git add ./local_data/*")
            with fabric_settings(warn_only=True):
                run('git commit -m "Local data commit from staging."')
                run("git push origin dev")

def update():
    if not env.host:
        abort("update can only be called on demo, staging and prod.")
    else:
        with cd(env.directory):
            with prefix(env.activate):
                if env.type=="staging":
                    commit_local_data()
                    run("git pull origin dev")
                elif env.type=="prod":
                    commit_prod_data()
                    run("git pull origin master")
                else:
                    run("git pull origin master")
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
                run("echo 'y'|python manage.py rebuild_index")
                restart_apache()
                run("chmod 777 logs/ -R")
                run("chmod 777 media/ -R")
