import os
import sys

from fabric.api import env, sudo, cd, run, local, settings as fabric_settings
from fabric.context_managers import prefix
from fabric.contrib import django as fabric_django
from fabric.utils import abort

ROOT = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
sys.path.append(ROOT)
fabric_django.settings_module('settings')
from django.conf import settings
from south.models import MigrationHistory


__all__= ["staging", "prod", "restart", "create_database", "load_prod_data", 
          "load_local_data", "commit_local_data", "commit_prod_data", "migrate",
          "update", "schemamigrate", "runserver"]

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
        if os.path.exists(ROOT + "/database.db"):
            os.remove(ROOT + "/database.db")
        local("python copy_media.py prod in")
        local("python manage.py syncdb --noinput --migrate")
    else:
        if env.host == "umeqo.com":
            abort("create_database cannot be called on prod.")
        with cd(env.directory):
            with prefix(env.activate):
                run('echo "DROP DATABASE umeqo_main; CREATE DATABASE umeqo_main;"|python manage.py dbshell')
                run("python manage.py syncdb --noinput --migrate")
                run("python copy_media.py prod in")
                
    
def schemamigrate():
    if not env.host:
        apps = list(set(app.app_name for app in MigrationHistory.objects.all()))
        with fabric_settings(warn_only=True):
            for app in apps:
                local("python manage.py schemamigration %s --auto" % app)
    else:
        abort("Update can only be called locally.")

def load_prod_data():
    if not env.host:  
        local("python copy_media.py prod in")
        local("python manage.py flush --noinput")
    else:
        with cd(env.directory):
            with prefix(env.activate):
                if env.host == "staging.umeqo.com":
                    abort("load_prod_data should not be called on staging.")
                run("python copy_media.py prod in")
                run("python manage.py flush --noinput")

def load_local_data():
    if not env.host:
        local("python copy_media.py local in")
        local("python manage.py loaddata %slocal_data.json" % (settings.LOCAL_FIXTURES_ROOT))    
    else:
        if env.host == "umeqo.com":
            abort("load_local_data should not be called on prod.")
        with cd(env.directory):
            with prefix(env.activate):
                run("python copy_media.py local in")
                run("python manage.py loaddata %slocal_data.json" % (settings.LOCAL_FIXTURES_ROOT))  

def commit_prod_data():
    if env.host != "staging.umeqo.com":
        abort("commit_prod_data should only be called on staging")
    with cd(env.directory):
        with prefix(env.activate):
            for app in settings.PROD_DATA_MODELS:
                model_labels = []
                if app == "sites":
                    run("python manage.py dumpdata sites --indent=1 > ./initial_data.json")
                    continue
                fixtures_dir = "%s/%s/fixtures" % (ROOT, app)
                print "about to create dir"
                if not os.path.exists(fixtures_dir):
                    print "creating dir"
                    os.makedirs(fixtures_dir)
                for model in settings.PROD_DATA_MODELS[app]:
                    model_labels.append("%s.%s" % (app, model))
                    with fabric_settings(warn_only=True):
                        run("python manage.py file_cleanup %s.%s" % (app, model))
                run("python manage.py dumpdata %s --indent=1 > %s/initial_data.json" % (" ".join(model_labels), fixtures_dir))
            run("python copy_media.py prod out")
            run("git add -A")
            with fabric_settings(warn_only=True):
                run('git commit -m "Local data commit from staging."')
                run("git push")

def runserver():
    if not env.host:
        if not os.path.exists(settings.CKEDITOR_UPLOAD_PATH):
            os.makedirs(settings.CKEDITOR_UPLOAD_PATH)
        local("python manage.py runserver")
    else: 
        abort("runserver can only be called locally.")

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
            if not os.path.exists("./local_data/fixtures/"):
                os.makedirs("./local_data/fixtures/")
            run("python manage.py dumpdata %s --indent=1 > ./local_data/fixtures/local_data.json" % (" ".join(model_labels)))
            run("git add -A")
            with fabric_settings(warn_only=True):
                run('git commit -m "Local data commit from staging."')
                run("git push")

def update():
    if env.host:
        with cd(env.directory):
            with prefix(env.activate):
                commit_local_data()
                commit_prod_data()
                run("git pull")
                run("python manage.py migrate --all")
                run("echo 'yes'|python manage.py collectstatic")
                """
                with fabric_settings(warn_only=True):
                    result = run("python manage.py test --setting=settings_test")
                if result.failed:
                    run("git reset --hard master@{1}")
                    run("python manage.py migrate --all")
                    #create_media_dirs()
                    run("echo 'yes'|python manage.py collectstatic")
                """
                restart()       
    else:
        abort("update cannot be called locally.")
