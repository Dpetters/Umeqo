import os, shutil, sys
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
          "update", "create_media_dirs", "schemamigrate"]

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
        local("find */migrations -name '*.pyc' | xargs rm")
        local("python manage.py migrate --all")
    else:
        abort("migrate can only be called locally.")
    
def create_database():
    create_media_dirs()
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

def create_media_dirs():
    for model_path in settings.MEDIA_MODEL_PATHS.split(" "):
        model_root = settings.MEDIA_ROOT + model_path
        if not os.path.exists(model_root):
            os.makedirs(model_root)
    
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
        for app in settings.LOCAL_DATA_APPS:
            local("python manage.py loaddata " + settings.LOCAL_FIXTURES_ROOT + "local_" + app + "_data.json")    
    else:
        with cd(env.directory):
            with prefix(env.activate):
                if env.host == "umeqo.com":
                    abort("load_local_data should not be called on prod.")
                run("python copy_media.py local in")
                for app in settings.LOCAL_DATA_APPS:
                    run("python manage.py loaddata  /var/www/umeqo/local_data/fixtures/local_" + app + "_data.json")

def commit_prod_data():
    if not env.host:
        abort("commit_prod_data should not be called locally.")
    else: 
        with cd(env.directory):
            with prefix(env.activate):
                run("python manage.py file_cleanup %s" % (settings.PROD_DATA_MODELS,))
                run("python copy_media.py prod out")
                run("python manage.py dumpdata sites --indent=1 > ./initial_data.json")
                run("python manage.py dumpdata core --indent=1 > ./core/fixtures/initial_data.json")
                run("git add -A")
                with fabric_settings(warn_only=True):
                    run('git commit -m "Prod data commit from staging."')
                    run("git push")

def commit_local_data():
    if not env.host:
        local("python manage.py file_cleanup %s" % (settings.LOCAL_DATA_MODELS,))
        local("python copy_media.py local out")
        for app in settings.LOCAL_DATA_APPS:
            # For some reason just running "loaddata user" works but "dumpdata user" doesn't. You need "dumpdata auth.user"
            if app == "user":
                local("python manage.py dumpdata auth.user --indent=1 > ./local_data/fixtures/local_user_data.json")
            else:
                local("python manage.py dumpdata " + app + " --indent=1 > ./local_data/fixtures/local_" + app + "_data.json")
    else: 
        if env.host == "umeqo.com":
            abort("commit_local_data should not be called on prod.")
        with cd(env.directory):
            with prefix(env.activate):
                run("python manage.py file_cleanup student.Student")
                run("python copy_media.py local out")
                for app in settings.LOCAL_DATA_APPS:
                    # For some reason just running "loaddata user" works but "dumpdata user" doesn't. You need "dumpdata auth.user"
                    if app == "user":
                        run("python manage.py dumpdata auth.user --indent=1 > ./local_data/fixtures/local_user_data.json")
                    else:
                        run("python manage.py dumpdata " + app + " --indent=1 > ./local_data/fixtures/local_" + app + "_data.json")
                run("git add -A")
                with fabric_settings(warn_only=True):
                    run('git commit -m "Local data commit from staging."')
                    run("git push")

def update():
    if env.host:
        with cd(env.directory):
            with prefix(env.activate):
                create_media_dirs()
                commit_local_data()
                commit_prod_data()
                run("git pull")
                run("python manage.py migrate --all")
                run("echo 'yes'|python manage.py collectstatic")
                """
                with fabric_settings(warn_only=True):
                    result = run("python manage.py test")
                if result.failed:
                    run("git reset --hard master@{1}")
                    run("python manage.py migrate --all")
                    create_media_dirs()
                    run("echo 'yes'|python manage.py collectstatic")
                """
                restart()       
    else:
        abort("update cannot be called locally.")