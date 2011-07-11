import datetime, Image
from django.conf import settings

def get_resume_filename(instance, filename):
    return "student/Student/" + instance.last_name + "_" + instance.first_name + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"

def get_campusorg_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "core/CampusOrg/" + instance.name.replace(" ", "_") + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension

def get_course_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "core/Course/" + instance.name.replace(" ", "_") + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension

def scale_down_image(image):
    filename = image.path
    image = Image.open(filename)
    ratio = min(float(settings.MAX_DIALOG_IMAGE_WIDTH)/image.width, float(settings.MAX_DIALOG_IMAGE_HEIGHT)/image.height)
    size = (int(ratio * image.width), int(ratio * image.height))
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(filename)