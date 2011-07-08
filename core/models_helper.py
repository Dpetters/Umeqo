import datetime
from django.conf import settings

def get_resume_filename(instance, filename):
    filename = settings.RESUMES_ROOT + instance.last_name + "_" + instance.first_name + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"
    return filename

def get_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    filename = settings.IMAGES_ROOT + instance.name.replace(" ", "_") + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension
    return filename