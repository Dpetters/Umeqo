from pyPdf import PdfFileReader

from django.conf import settings as s
from django.core.management.base import BaseCommand

from core.email import send_html_mail
from student.models import Student

"""
This script was created before we validated submitted resumes against PdfFileReader explicitely.
It goes through all visible (to the recruiters) students and checks each of their resumes.
The student's whose resumes could not be read have their accounts deactivated so that their
resume does not break resume book delivery. The admins are also notified.

It's running as a cronjob atm but will be retired once the new validation gets thoroughly tested.
"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        for student in Student.objects.visible():
            try:
                PdfFileReader(file("%s%s" % (s.MEDIA_ROOT, str(student.resume)), "rb"),)
            except Exception as e:
                student.deactivate()
                managers = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                send_html_mail("[Umeqo] Faulty Resume", "%s %s' resume was faulty. \
                The account was suspended. Go and fix the resume!" \
                 % (student.first_name, student.last_name), managers)
