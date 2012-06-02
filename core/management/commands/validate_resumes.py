from pyPdf import PdfFileReader

from django.conf import settings as s
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import render_to_string

from core.email import get_basic_email_context, send_email
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
                try:
                    student.deactivate()
                    
                    managers = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                    
                    context = Context({
                        'student_first_name': student.first_name,
                        'student_last_name': student.last_name,
                        'student_email': student.user.email
                    })
                    context.update(get_basic_email_context())
                    
                    subject = ''.join(render_to_string('email_admin_subject.txt', {
                        'message': "Faulty resume"
                    }, context).splitlines())
    
                    body = render_to_string('faulty_resume_email_body.txt', context)
            
                    send_email(subject, body, managers)
                except Exception as e:
                    print e