import datetime

def get_resume_book_filename(instance, filename):
    return "%s/%s_%s_%s_%s.pdf" % (str(type(instance)._meta.replace(".", "/")), instance.recruiter.user.first_name.lower(), instance.recruiter.user.last_name.lower(), instance.recruiter.user, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

def get_logo_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s/%s_%s%s" % (str(type(instance)._meta.replace(".", "/")), instance.name.lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)