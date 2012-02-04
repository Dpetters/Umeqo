from pyPdf import PdfFileReader

from django.conf import settings as s
from django.core.management.base import BaseCommand

from core.email import send_html_mail
from student.models import Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        for student in Student.objects.visible():
            try:
                PdfFileReader(file("%s%s" % (s.MEDIA_ROOT, str(student.resume)), "rb"),)
            except Exception as e:
                student.suspend()
                for rb in student.resumebook_set.filter(delivered=False):
                    rb.students.remove(student)
                    rb.save()
                student.save()
                managers = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                send_html_mail("[Umeqo] Faulty Resume", "%s %s' resume was faulty. The account was suspended. Go and fix the resume!" % (student.first_name, student.last_name), managers)
                