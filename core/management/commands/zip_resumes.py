import os
import re
import shutil

from time import strftime, gmtime

from django.conf import settings as s
from django.core.management.base import BaseCommand

from core.file_utils import find_first_file
from core.models import School
from core.zip import create_zip
from events.models import Event
from student.models import Student


def zip_resumes():
    now = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    print "zipping resumes %s on %s" % (s.SITE_NAME, now)
    try:
        all_resumes_dir = "%s%s/" % (s.ZIPPED_RESUMES_DIRECTORY, s.ALL_ZIPPED_RESUMES_FILENAME_START)
        if not os.path.exists(all_resumes_dir):
            os.makedirs(all_resumes_dir)
        for school in School.objects.filter(name="Massachusetts Institute of Technology"):
            students = Student.objects.filter(profile_created=True, user__is_active=True)
            school_dir = "%s%s/" % (all_resumes_dir, school.name)
            if not os.path.exists(school_dir):
                os.makedirs(school_dir)
            for student in students:
                student_resume_file_name = "%s %s %s.pdf" % (student.first_name, student.last_name, student.user.email)
                shutil.copyfile("%s%s" % (s.MEDIA_ROOT, student.resume.name), "%s%s" % (school_dir, student_resume_file_name))
            old_zip_file = find_first_file(s.ZIPPED_RESUMES_DIRECTORY, "%s.*.zip" % s.ALL_ZIPPED_RESUMES_FILENAME_START)
            create_zip(all_resumes_dir, "", "%s%s %s.zip" % (s.ZIPPED_RESUMES_DIRECTORY, s.ALL_ZIPPED_RESUMES_FILENAME_START, now))
            if old_zip_file:
                 os.remove(old_zip_file)
        event_resumes_dir = "%sevent_resumes/" % s.ZIPPED_RESUMES_DIRECTORY
        if not os.path.exists(event_resumes_dir):
            os.makedirs(event_resumes_dir)
        for event in Event.objects.all():
            event_dir_name = "%s (%d) All Participants" % (event.name, event.id)
            event_dir = "%s%s" % (event_resumes_dir, event_dir_name)
            if not os.path.exists(event_dir):
                os.makedirs(event_dir)
            for student in event.all_participants():
                student_resume_file_name = "%s %s %s.pdf" % (student.first_name, student.last_name, student.user.email)
                shutil.copyfile("%s%s" % (s.MEDIA_ROOT, student.resume.name), "%s/%s" % (event_dir, student_resume_file_name))
            old_zip_file = find_first_file(event_resumes_dir, "%s.*.zip" % re.escape(event_dir_name))
            create_zip(event_dir, "", "%s %s.zip" % (event_dir, now))
            if old_zip_file:
                 os.remove(old_zip_file)

    except Exception as e:
        print "failed to zip resumes on: %s " % str(e)
    else:
        print "successfully zipped resumes"


class Command(BaseCommand):    
    def handle(self, *args, **options):
        zip_resumes()
