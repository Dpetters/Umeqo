"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

""" 
This script is meant to dump newly-added fake non-fixturable data to what we already have.
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
if os.path.exists("./local_data/local_xapian_index/"):
    delete_contents("./local_data/local_xapian_index/")
    os.rmdir("./local_data/local_xapian_index/")

# Delete the old submitted resumes
if os.path.exists("./local_data/media/local_submitted_resumes/"):
    delete_contents("./local_data/media/local_submitted_resumes/")
    os.rmdir("./local_data/media/local_submitted_resumes/")

# Delete the old submitted user images
if os.path.exists("./local_data/media/local_submitted_user_images/"):
    delete_contents("./local_data/media/local_submitted_user_images/")
    os.rmdir("./local_data/media/local_submitted_user_images/")

shutil.copytree("./xapian_index/", "./local_data/local_xapian_index/")
shutil.copytree("./media/submitted_resumes/", "./local_data/media/local_submitted_resumes/")
shutil.copytree("./media/submitted_user_images/", "./local_data/media/local_submitted_user_images/")

for app in settings.LOCAL_SETTINGS_APPS:
    # For some reason just putting user down on loaddata works but for dumpdata you need auth.user
    if app == "user":
        p = subprocess.Popen("python manage.py dumpdata auth.user --indent=1 > ./local_data/fixtures/local_user_data.json", shell=True)
    else:
        p = subprocess.Popen("python manage.py dumpdata " + app + " --indent=1 > ./local_data/fixtures/local_" + app + "_data.json", shell=True)
    p.wait()