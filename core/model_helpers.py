import datetime, Image
from django.conf import settings

def get_resume_filename(instance, filename):
    return "%s%s_%s_%s_%s.pdf" % (settings.STUDENT_STUDENT_PATH, instance.last_name.lower(), instance.first_name.lower(), str(instance.user).lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

def get_campus_org_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s%s" % (settings.CORE_CAMPUS_ORG_PATH, instance.name.replace(" ", "_").lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)

def get_course_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s%s" % (settings.CORE_COURSE_PATH, instance.name.replace(" ", "_").lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)

def scale_down_image(image):
    filename = image.path
    image = Image.open(filename)
    ratio = min(float(settings.MAX_DIALOG_IMAGE_WIDTH)/image.width, float(settings.MAX_DIALOG_IMAGE_HEIGHT)/image.height)
    size = (int(ratio * image.width), int(ratio * image.height))
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(filename)