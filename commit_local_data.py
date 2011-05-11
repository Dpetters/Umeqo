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

# Delete old search index files
if os.path.exists(settings.HAYSTACK_XAPIAN_PATH):
    delete_contents(settings.HAYSTACK_XAPIAN_PATH)
    os.rmdir(settings.HAYSTACK_XAPIAN_PATH)

# Delete the old submitted resumes
submitted_resumes_path = ROOT + "/media/submitted_resumes/"
if os.path.exists(submitted_resumes_path):
    delete_contents(submitted_resumes_path)
    os.rmdir(submitted_resumes_path)

# Delete the old submitted user images
submitted_user_images_path = ROOT + "/media/submitted_user_images/"
if os.path.exists(submitted_user_images_path):
    delete_contents(submitted_user_images_path)
    os.rmdir(submitted_user_images_path)

shutil.copytree("./local_data/xapian_index/", "./xapian_index/")
shutil.copytree("./local_data/media/submitted_resumes/", "./media/submitted_resumes/")
shutil.copytree("./local_data/media/submitted_user_images/", "./media/submitted_user_images/")

p = subprocess.Popen("python manage.py syncdb --noinput --migrate", shell=True)
p.wait()

for app in settings.LOCAL_SETTINGS_APPS:
    print "python manage.py loaddata ./local_data/fixtures/local_" + app + "_data.json"
    p = subprocess.Popen("python manage.py loaddata ./local_data/fixtures/local_" + app + "_data.json", shell=True)
    p.wait()