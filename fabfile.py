import os, subprocess, shutil, sys
from fabric.api import local, lcd, abort
from fabric.contrib.console import confirm
from fabric.contrib import django as fabric_django

ROOT = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
sys.path.append(ROOT)
fabric_django.settings_module('settings')
from django.conf import settings

__all__= ["refresh_database", "commit_local_data"]

def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
"""
def run_server():
    subprocess.Popen("python manage.py runserver", shell=True)

def run_memcached():
    subprocess.Popen("memcached", shell=True)

def run_solr():
    os.chdir(ROOT +"/apache-solr-1.4.1/")
    subprocess.Popen("java -jar start.jar", shell=True)

def run_local():
    run_server()
    run_memcached()
    run_solr()
"""
def refresh_database():
    if os.path.exists("./database.db"):
        os.remove("./database.db")

    # Delete existing resumes and the parent directory
    # copytree requires that that directory doesn't exist
    submitted_resumes_path = ROOT + "/media/resumes/"
    if os.path.exists(submitted_resumes_path):
        delete_contents(submitted_resumes_path)
        os.rmdir(submitted_resumes_path)

    # Create the local resumes directory
    # copytree requires that it exists
    local_data_submitted_resumes_path = ROOT + "/local_data/media/resumes/"
    if not os.path.exists(local_data_submitted_resumes_path):
        os.mkdir(local_data_submitted_resumes_path)

    shutil.copytree(local_data_submitted_resumes_path, submitted_resumes_path)

    # Delete existing user images and the parent directory.
    # copytree requres that that directory doesn't exist
    submitted_user_images_path = ROOT + "/media/images/"
    if os.path.exists(submitted_user_images_path):
        delete_contents(submitted_user_images_path)
        os.rmdir(submitted_user_images_path)

    # Create the local images directory
    # copytree requires that it exists
    local_data_images_path = ROOT + "/local_data/media/images/"
    if not os.path.exists(local_data_images_path):
        os.mkdir(local_data_images_path)

    shutil.copytree(local_data_images_path, submitted_user_images_path)

    p = subprocess.Popen("python manage.py syncdb --noinput --migrate", shell=True)
    p.wait()

    #os.chdir(ROOT +"/apache-solr-1.4.1/example/")
    #solr_proc = subprocess.Popen(["java", "-jar", "start.jar"], cwd=ROOT +"/apache-solr-1.4.1/")
    
    for app in settings.LOCAL_SETTINGS_APPS:
        p = subprocess.Popen("python manage.py loaddata ./local_data/fixtures/local_" + app + "_data.json", shell=True)
        p.wait()
        
    #solr_proc.kill()


def commit_local_data():
    print 'This script might overwrite local data that has already been created. \
            \n To avoid this, make sure that you have done things in the following order. \
            \n 1. Pulled from git to make sure you have the latest local_data. \
            \n 2. Ran "fab refresh_database" to integrate the local_data. \
            \n 3. Now, having the latest local data, you created new your local data. \
            \n 4. And are now running this script to save it!.'
    
    if not confirm("Continue anyway?"):
        abort("Aborting at user request.")

    # Delete existing local data resumes and the parent directory
    # copytree requires that that directory doesn't exist
    local_data_submitted_resumes_path = ROOT + "/local_data/media/resumes/"
    if os.path.exists(local_data_submitted_resumes_path):
        delete_contents(local_data_submitted_resumes_path)
        os.rmdir(local_data_submitted_resumes_path)

    # Create the submitted resumes directory
    # copytree requires that it exists
    submitted_resumes_path = ROOT + "/media/resumes/"
    if not os.path.exists(submitted_resumes_path):
        os.mkdir(submitted_resumes_path)  
    
    shutil.copytree(submitted_resumes_path, local_data_submitted_resumes_path)
    
    # Delete existing local user images and the parent directory.
    # copytree requres that that directory doesn't exist
    local_data_images_path = ROOT + "/local_data/media/images/"
    if os.path.exists(local_data_images_path):
        delete_contents(local_data_images_path)
        os.rmdir(local_data_images_path)

    # Create the submitted images directory
    # copytree requires that it exists
    submitted_user_images_path = ROOT + "/media/images/"
    if not os.path.exists(submitted_user_images_path):
        os.mkdir(submitted_user_images_path)  
        
    shutil.copytree(submitted_user_images_path,  local_data_images_path)
    
    local_data_fixtures_path = "./local_data/fixtures/"
    if not os.path.exists(local_data_fixtures_path):
        os.mkdir(local_data_fixtures_path)
        
    for app in settings.LOCAL_SETTINGS_APPS:
        # For some reason just running "loaddata user" works but "dumpdata user" doesn't. You need "dumpdata auth.user"
        if app == "user":
            p = subprocess.Popen("python manage.py dumpdata auth.user --indent=1 > ./local_data/fixtures/local_user_data.json", shell=True)
        else:
            p = subprocess.Popen("python manage.py dumpdata " + app + " --indent=1 > ./local_data/fixtures/local_" + app + "_data.json", shell=True)
        p.wait()