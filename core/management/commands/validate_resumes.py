from datetime import datetime, timedelta

from pyPdf import PdfFileReader

from django.conf import settings as s
from django.core.management.base import BaseCommand

from student.models import Student


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for student in Student.objects.filter(profile_created=True):
            try:
                resume = PdfFileReader(file("%s%s" % (s.MEDIA_ROOT, str(student.resume))))
            except:
                