from django.conf import settings as s

from django.core.management.base import BaseCommand, CommandError
from student.view_helpers import resume_processing_helper

class Command(BaseCommand):
    args = '<resume_name>'
    help = 'Provide a resume name to check if it can be parsed.)'

    def handle(self, *args, **options):
        if (len(args)==0):
            raise CommandError("You must provide a resume book name.")
        elif(len(args)> 1):
            raise CommandError("You must only provide one resume book name.")
        print resume_processing_helper("%sstudent/student/%s" % (s.MEDIA_ROOT, args[0]))