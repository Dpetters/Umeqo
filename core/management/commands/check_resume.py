import os

from pyPdf import PdfFileReader

from django.conf import settings as s
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<resume_name>'
    help = 'Provide a resume name to check if it can be parsed.)'

    def handle(self, *args, **options):
        if (len(args)==0):
            raise CommandError("You must provide a resume book name.")
        elif(len(args)> 1):
            raise CommandError("You must only provide one resume book name.")
        filepath = "%sstudent/student/%s" % (s.MEDIA_ROOT, args[0])
        if not os.path.exists(filepath):
            raise CommandError("There is no resume in MEDIA_ROOT/student/student/ with the name you provided.")
        try:
            file = open(filepath, "rb")
            PdfFileReader(file)
            file.close()
        except Exception as e:
            print "BROKEN (could not be opened by PdfFileReader)"
        else:
            print "VALID (PdfFileReader was able to open it)"