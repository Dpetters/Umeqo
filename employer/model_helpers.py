import datetime
import os

def get_resume_book_filename(instance, filename):
    parts = os.path.basename(filename).split(".")
    extension = parts[-1]
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return "%s/%s_%s.%s" % (str(type(instance)._meta).replace(".", "/"),
                            instance.recruiter.user.username, now, extension)

def get_logo_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s/%s_%s%s" % (str(type(instance)._meta).replace(".", "/"), instance.name.lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)