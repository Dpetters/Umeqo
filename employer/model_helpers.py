import datetime
import os

def get_resume_book_filename(instance, filename):
    parts = os.path.basename(filename).split(".")
    if parts[-2] == "pdf":
        return  ".".join(parts[:-1])
    return "%s/%s_%s.pdf" % (str(type(instance)._meta).replace(".", "/"), str(instance.recruiter.user)[:18], datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

def get_logo_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s/%s_%s%s" % (str(type(instance)._meta).replace(".", "/"), instance.name.lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)