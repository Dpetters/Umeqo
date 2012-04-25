from datetime import datetime
import os
import shutil

from django.conf import settings as s
from django.core.management.base import BaseCommand

from core.zip import create_zip
from student.models import Student

class Command(BaseCommand):
    
    def handle(self, *args, **options):
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
                create_zip(resume_dir, "", "%s/All Umeqo Resumes %s.zip" % (s.MEDIA_ROOT, datetime.now().strftime("%Y-%b-%d %H-%M-%S")))
        except Exception as e:
            print e