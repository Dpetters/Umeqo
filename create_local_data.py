"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

""" 
This script is meant to populate the database with some fake non-fixturable data.
"""

import os, subprocess, shutil

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
ROOT = os.path.dirname(os.path.realpath("__file__"))

from django.conf import settings

# Helper Function
def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# Delete old search index files.
# New index files get created automatically when loaddata gets run below
if os.path.exists(settings.HAYSTACK_WHOOSH_PATH):
    delete_contents(settings.HAYSTACK_WHOOSH_PATH)

# Delete the old submitted resumes. Also delete the directory if it exists because
# copytree below will throw a fit if it already exists
submitted_resumes_path = ROOT + "/media/submitted_resumes/"
if os.path.exists(submitted_resumes_path):
    delete_contents(submitted_resumes_path)
    os.rmdir(submitted_resumes_path)

local_data_submitted_resumes_path = "./local_data/media/local_submitted_resumes/"
if not os.path.exists(local_data_submitted_resumes_path):
    os.mkdir(local_data_submitted_resumes_path)  

shutil.copytree(local_data_submitted_resumes_path, submitted_resumes_path)

# Delete the old submitted user images. Also delete the directory if it exists because
# copytree below will throw a fit if it already exists
submitted_user_images_path = ROOT + "/media/submitted_user_images/"
if os.path.exists(submitted_user_images_path):
    delete_contents(submitted_user_images_path)
    os.rmdir(submitted_user_images_path)

local_data_submitted_user_images_path = "./local_data/media/local_submitted_resumes/"
if not os.path.exists(local_data_submitted_user_images_path):
    os.mkdir(local_data_submitted_user_images_path)  
    
shutil.copytree(local_data_submitted_user_images_path, submitted_user_images_path)


p = subprocess.Popen("python manage.py syncdb --noinput --migrate", shell=True)
p.wait()

for app in settings.LOCAL_SETTINGS_APPS:
    p = subprocess.Popen("python manage.py loaddata ./local_data/fixtures/local_" + app + "_data.json", shell=True)
    p.wait()