import datetime, Image
from django.conf import settings

def get_resume_filename(instance, filename):
    filename = "student/Student/" + instance.last_name.lower() + "_" + instance.first_name.lower() + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"
    print filename
    return filename

def get_campusorg_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    filename = "core/CampusOrg/" + instance.name.replace(" ", "_").lower() + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension
    return filename

def get_course_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    filename = "core/Course/" + instance.name.replace(" ", "_").lower() + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension
    return filename

def scale_down_image(image):
    filename = image.path
    image = Image.open(filename)
    ratio = min(float(settings.MAX_DIALOG_IMAGE_WIDTH)/image.width, float(settings.MAX_DIALOG_IMAGE_HEIGHT)/image.height)
    size = (int(ratio * image.width), int(ratio * image.height))
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(filename)