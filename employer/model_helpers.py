import datetime
from django.conf import settings

def get_resume_book_filename(instance, filename):
    return "%s%s_%s_%s_%s.pdf" % (settings.EMPLOYER_RESUME_BOOK_PATH, instance.recruiter.user.first_name.lower(), instance.recruiter.user.last_name.lower(), instance.recruiter.user, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

def get_logo_filename(instance, filename):
    extension = filename[filename.find('.'):]
    return "%s%s_%s%s" % (settings.EMPLOYER_EMPLOYER_PATH, instance.name.lower(), datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), extension)