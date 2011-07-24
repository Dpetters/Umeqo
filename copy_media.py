import os, shutil
from optparse import OptionParser

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

def main():
    usage = "usage: %prog [options] type in_or_out"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        parser.error("You must if you're moving local or prod data and if u want it copied in or out.")
    
    if args[0] == "prod":
        root = settings.PROD_MEDIA_ROOT
        apps = settings.PROD_DATA_APPS
    else:
        root = settings.LOCAL_MEDIA_ROOT
        apps = settings.LOCAL_DATA_APPS    

    if args[1] == "in":
        copy_in_media(root, apps)
    else:
        copy_out_media(root, apps)
    
def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def copy_in_media(root, apps):
    if not os.path.exists(root):
        os.makedirs(root)
        
    for app in apps:
        if not os.path.exists(root + app):
            os.makedirs(root + app)
        if os.path.exists(settings.MEDIA_ROOT + app):
            delete_contents(settings.MEDIA_ROOT + app)
            os.rmdir(settings.MEDIA_ROOT + app)
        shutil.copytree(root + app, settings.MEDIA_ROOT + app)

def copy_out_media(root, apps):
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    if os.path.exists(root):
        delete_contents(root)
    else:
        os.makedirs(root)
        
    for app in apps:
        if not os.path.exists(settings.MEDIA_ROOT + app):
            os.makedirs(settings.MEDIA_ROOT + app)
        shutil.copytree(settings.MEDIA_ROOT + app, root + app)
        

if __name__ == "__main__":
    main()