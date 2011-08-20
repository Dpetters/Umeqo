import os, shutil
from optparse import OptionParser

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

def main():
    usage = "usage: %prog [options] type in_or_out"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        parser.error("You must specify whether you're moving local or prod data and if u want it copied in or out.")
    
    if args[0] == "prod":
        root = settings.PROD_MEDIA_ROOT
        model_paths = []
        for app in settings.PROD_DATA_MODELS:
            for model in settings.PROD_DATA_MODELS[app]:
                model_paths.append("%s/%s" % (app, model))
    else:
        root = settings.LOCAL_MEDIA_ROOT
        model_paths = []
        for app in settings.LOCAL_DATA_MODELS:
            for model in settings.LOCAL_DATA_MODELS[app]:
                model_paths.append("%s/%s" % (app, model))
        
    if args[1] == "in":
        copy_in_media(root, model_paths)
    else:
        copy_out_media(root, model_paths)
    
def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def copy_in_media(root, model_paths):
    if not os.path.exists(root):
        os.makedirs(root)
    for model_path in model_paths:
        data_path = os.path.normpath(root + model_path)
        media_path = os.path.normpath(settings.MEDIA_ROOT + model_path)
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        if os.path.exists(media_path):
            delete_contents(media_path)
            os.rmdir(media_path)
        shutil.copytree(data_path, media_path)

def copy_out_media(root, model_paths):
    if os.path.exists(root):
        delete_contents(root)
    else:
        os.makedirs(root)
    for model_path in model_paths:
        data_path = os.path.normpath(root + model_path)
        media_path = os.path.normpath(settings.MEDIA_ROOT + model_path)
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        shutil.copytree(media_path, data_path)

if __name__ == "__main__":
    main()