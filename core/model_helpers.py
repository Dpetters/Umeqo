import datetime
import Image
import os

from django.core.files import File
from django.conf import settings

def get_resume_filename(instance, filename):
    return "%s%s_%s_%s_%s.pdf" % (settings.STUDENT_STUDENT_PATH, instance.last_name.lower(), instance.first_name.lower(), str(instance.user).lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

def get_campus_org_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s%s" % (settings.CORE_CAMPUS_ORG_PATH, instance.name.replace(" ", "_").lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)

def get_course_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s%s" % (settings.CORE_COURSE_PATH, instance.name.replace(" ", "_").lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)

def get_campus_org_thumbnail_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s_thumbnail%s" % (settings.CORE_CAMPUS_ORG_PATH, instance.name.replace(" ", "_").lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)

def get_course_thumbnail_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s_thumbnail%s" % (settings.CORE_COURSE_PATH, instance.name.replace(" ", "_").lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)

def generate_thumbnail(image):
    image_path = image.path
    image = Image.open(image_path)
    width, height = image.size
    ratio = min(float(settings.MAX_DIALOG_IMAGE_WIDTH)/width, float(settings.MAX_DIALOG_IMAGE_HEIGHT)/height)
    size = (int(ratio * width), int(ratio * height))
    image.thumbnail(size, Image.ANTIALIAS)
    extension = image_path[image_path.find('.'):]
    thumbnail_full_path = "%s%s_tmp%s" % (os.path.dirname(image_path), os.path.basename(image_path).split(".")[0], extension)
    image.save(thumbnail_full_path)
    return thumbnail_full_path, File(file(thumbnail_full_path, "rb"))