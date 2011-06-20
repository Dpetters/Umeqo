"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
import datetime, Image
from django.conf import settings

def get_resume_filename(instance, filename):
    filename = settings.SUBMITTED_RESUME_ROOT + instance.last_name + "_" + instance.first_name + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"
    return filename

def get_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    filename = "content/images/" + instance.name.replace(" ", "_") + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension
    return filename

def resize_image(instance, max_width, max_height):
    if instance.image:
        filename = instance.image.path
        image = Image.open(filename)
        ratio = min(float(max_width)/instance.image.width, float(max_height)/instance.image.height)
        size = (int(ratio * instance.image.width), int(ratio * instance.image.height))
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)