import os
import shutil
from string import rsplit

from optparse import make_option
from django.conf import settings
from django.core.management.base import CommandError, LabelCommand
from django.db import models
from django.utils.encoding import smart_unicode
from core.utils import parse_apps_and_models, get_model_cls

class Command(LabelCommand):
    args = '<appname.Model> [appname.Model] ...>'
    help = ("Cleans orphaned file field files from <upload-path>.\n"
            "'Orphaned' is defined as existing under <upload-path> "
            "but\nnot referenced by any file fields in given "
            "<appname.Model>s.")
    option_list = LabelCommand.option_list + (
        make_option('--move-to', '-m', action='store', dest='backup_to',
            help='Instead of removing, move the files to the given location.'),
    )

    def handle_label(self, label, **options):
        filenames_on_disk = set()
        filenames_in_database = set()
        for appname, modelname in parse_apps_and_models(label):
            file_path = settings.MEDIA_ROOT + appname + "/" + modelname
            file_path = file_path.lower()
            filenames_on_disk.update(list_files(file_path))
            model = get_model_cls(appname, modelname)
            filefields = get_filefields(model)
            if not filefields:
                raise CommandError("Model %s.%s contains no file fields" % (appname, modelname))
            for filefield in filefields:
                kwargs = {filefield: ''}
                qs = model.objects.exclude(**kwargs).values_list(filefield, flat=True)
                filenames_in_database.update(os.path.join(settings.MEDIA_ROOT, name) for name in qs)
        
        db_has_unseen_files = filenames_in_database.issubset(filenames_on_disk)

        if not db_has_unseen_files:
            print filenames_in_database - filenames_on_disk
            raise CommandError("Database filenames are not a "
                                "subset of actual filenames on disk. Will not risk "
                                "erasing arbitrary files, exiting.")
        
        dangling_files = filenames_on_disk - filenames_in_database
        print "Cleaning up %d files." % len(dangling_files)
        
        if options['backup_to']:
            move_files(dangling_files, options['backup_to'])
        else:
            remove_files(dangling_files)

def get_filefields(model_cls):
    filefields = []
    for field in model_cls._meta.fields:
        if issubclass(type(field), models.FileField):
            filefields.append(field.name)
    return filefields

def list_files(base_path):
    files = set()
    for (root, dirnames, filenames) in os.walk(base_path):
        files.update(smart_unicode(os.path.join(root, name)).replace("\\", "/") for name in filenames)
    return files

def move_files(filenames, backup_dir):
    for name in filenames:
        dir = rsplit(backup_dir + name.split(settings.MEDIA_ROOT)[1], '\\', 1)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(name, backup_dir + name.split(settings.MEDIA_ROOT)[1])
    remove_files(filenames)

def remove_files(filenames):
    for name in filenames:
        os.remove(name)