import os
import shutil

from datetime import datetime

from django.conf import settings as s
from django.core.management.base import BaseCommand

from core.file_utils import find_first_file
from core.zip import create_zip
from student.models import Student


def zip_resumes():
    try:
        for school in ['mit']:
            resume_dir = "%sresumes" % s.MEDIA_ROOT
            students = Student.objects.filter(profile_created=True, user__is_active=True)
            school_dir = "%s/%s" % (resume_dir, school)
            if not os.path.exists(school_dir):
                os.makedirs(school_dir)
            for student in students:
                file_name = "%s %s %s.pdf" % (student.first_name, student.last_name, student.user.email)
                shutil.copyfile("%s/%s" % (s.MEDIA_ROOT, student.resume.name), "%s/%s" %(school_dir, file_name))
            old_zip_file = find_first_file(s.MEDIA_ROOT, "%s.*.zip" % s.ALL_ZIPPED_RESUMES_FILENAME_START)
            create_zip(resume_dir, "", "%s/%s %s.zip" % (s.MEDIA_ROOT, s.ALL_ZIPPED_RESUMES_FILENAME_START, datetime.now().strftime("%Y-%b-%d %H-%M-%S")))
            os.remove(old_zip_file)
    except Exception as e:
        print e


class Command(BaseCommand):    
    def handle(self, *args, **options):
        zip_resumes()