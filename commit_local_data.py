"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

""" 
This script is meant to dump newly-added fake non-fixturable data to what we already have.
"""

c  = raw_input('Make sure that you ran "create_local_data.py" then created the new local data, and only then are running this script in that order.\n\
Otherwise you risk overwriting existing local data. Press lowercase "y" to continue.\n\'')

if not c=='y':
    exit()
    
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

# Delete old local_data search index files. Also delete the directory if it exists because
# copytree below will throw a fit if it already exists
if os.path.exists("./local_data/local_xapian_index/"):
    delete_contents("./local_data/local_xapian_index/")
    os.rmdir("./local_data/local_xapian_index/")

if not os.path.exists(settings.HAYSTACK_XAPIAN_PATH):
    os.mkdir(settings.HAYSTACK_XAPIAN_PATH)

shutil.copytree(settings.HAYSTACK_XAPIAN_PATH, "./local_data/local_xapian_index/")

# Delete the old local_data submitted resumes. Also delete the directory if it exists because
# copytree below will throw a fit if it already exists
if os.path.exists("./local_data/media/local_submitted_resumes/"):
    delete_contents("./local_data/media/local_submitted_resumes/")
    os.rmdir("./local_data/media/local_submitted_resumes/")

submitted_resumes_path = ROOT + "/media/submitted_resumes/"
if not os.path.exists(submitted_resumes_path):
    os.mkdir(submitted_resumes_path)  

shutil.copytree(submitted_resumes_path, "./local_data/media/local_submitted_resumes/")

# Delete the old local_data submitted user images. Also delete the directory if it exists because
# copytree below will throw a fit if it already exists
if os.path.exists("./local_data/media/local_submitted_user_images/"):
    delete_contents("./local_data/media/local_submitted_user_images/")
    os.rmdir("./local_data/media/local_submitted_user_images/")

submitted_user_images_path = ROOT + "/media/submitted_user_images/"
if not os.path.exists(submitted_user_images_path):
    os.mkdir(submitted_user_images_path)  
    
shutil.copytree(submitted_user_images_path, "./local_data/media/local_submitted_user_images/")

for app in settings.LOCAL_SETTINGS_APPS:
    # For some reason just running "loaddata user" works but "dumpdata user" doesn't. You need "dumpdata auth.user"
    if app == "user":
        p = subprocess.Popen("python manage.py dumpdata auth.user --indent=1 > ./local_data/fixtures/local_user_data.json", shell=True)
    else:
        p = subprocess.Popen("python manage.py dumpdata " + app + " --indent=1 > ./local_data/fixtures/local_" + app + "_data.json", shell=True)
    p.wait()