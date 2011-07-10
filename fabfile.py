import os, subprocess, shutil, sys
from fabric.api import env, sudo
from fabric.contrib import django as fabric_django

ROOT = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
sys.path.append(ROOT)
fabric_django.settings_module('settings')
from django.conf import settings


__all__= ["staging", "prod", "reboot", "create_database", "update_database", 
          "load_local_data", "commit_local_data", "commit_prod_data"]


def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def staging():
    env.hosts = ['root@staging.umeqo.com']


def prod():
    env.hosts = ['root@umeqo.com']


def reboot(): 
    sudo('service apache2 restart')
    sudo('service nginx restart')


def copy_in_local_media():
    for app in settings.LOCAL_DATA_APPS:
        if os.path.exists(settings.MEDIA_ROOT + app):
            delete_contents(settings.MEDIA_ROOT + app)
    if os.path.exists(settings.MEDIA_ROOT):
        os.rmdir(settings.MEDIA_ROOT)

    if not os.path.exists(settings.LOCAL_DATA_ROOT):
        os.makedirs(settings.LOCAL_DATA_ROOT)

    shutil.copytree(settings.LOCAL_DATA_ROOT, settings.MEDIA_ROOT)


def copy_out_local_media():
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    for app in settings.LOCAL_DATA_APPS:
        if not os.path.exists(settings.MEDIA_ROOT + app):
            os.makedirs(settings.MEDIA_ROOT + app)
            
    if os.path.exists(settings.LOCAL_DATA_ROOT):
        os.rmdir(settings.LOCAL_DATA_ROOT)

    shutil.copytree(settings.MEDIA_ROOT, settings.LOCAL_DATA_ROOT)

    
def copy_in_prod_media():
    delete_contents(settings.MEDIA_ROOT)
    os.rmdir(settings.MEDIA_ROOT)   
    if not os.path.exists(settings.PROD_DATA_ROOT):
        os.makedirs(settings.PROD_DATA_ROOT)

    shutil.copytree(settings.PROD_DATA_ROOT, settings.MEDIA_ROOT)


def copy_out_prod_media():
    delete_contents(settings.PROD_DATA_ROOT)
    os.rmdir(settings.PROD_DATA_ROOT)   
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    shutil.copytree(settings.MEDIA_ROOT, settings.PROD_DATA_ROOT)


def create_database():
    if os.path.exists(ROOT + "/database.db"):
        os.remove(ROOT + "/database.db")
    copy_in_prod_media()
    p = subprocess.Popen("python manage.py syncdb --noinput --migrate", shell=True)
    p.wait()


def update_database():
    if not os.path.exists(ROOT + "/database.db"):
        create_database()
    else:
        copy_in_prod_media()
        p = subprocess.Popen("python manage.py flush --noinput", shell=True)
        p.wait()


def load_local_data():
    copy_in_local_media()
    for app in settings.LOCAL_DATA_APPS:
        p = subprocess.Popen("python manage.py loaddata " + settings.LOCAL_DATA_ROOT + "fixtures/local_" + app + "_data.json", shell=True)
        p.wait()


def commit_prod_data():
    p = subprocess.Popen("python manage.py file_cleanup core.CampusOrg core.Course", shell=True)
    p.wait()
    copy_out_prod_media()
    p = subprocess.Popen("python manage.py dumpdata sites --indent=1 > ./initial_data.json", shell=True)
    p.wait()
    p = subprocess.Popen("python manage.py dumpdata core --indent=1 > ./core/fixtures/initial_data.json", shell=True)
    p.wait()


def commit_local_data():
    p = subprocess.Popen("python manage.py file_cleanup events.Event student.Student employer.Employer", shell=True)
    p.wait()
    copy_out_local_media()
    for app in settings.LOCAL_DATA_APPS:
        # For some reason just running "loaddata user" works but "dumpdata user" doesn't. You need "dumpdata auth.user"
        if app == "user":
            p = subprocess.Popen("python manage.py dumpdata auth.user --indent=1 > ./local_data/fixtures/local_user_data.json", shell=True)
        else:
            p = subprocess.Popen("python manage.py dumpdata " + app + " --indent=1 > ./local_data/fixtures/local_" + app + "_data.json", shell=True)
        p.wait()