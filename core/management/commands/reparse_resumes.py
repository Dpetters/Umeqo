import os
import re
import subprocess

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from student.models import Student

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--win', action='store_true', dest='win', default=False, help='Use the version of pdftotext for windows.'),
    )
    
    def handle(self, *args, **options):
        failed = []
        for student in Student.objects.filter(profile_created=True, user__is_active=True):
            try:
                pdf_file_path = settings.MEDIA_ROOT + student.resume.name
                txt_file_path = pdf_file_path.replace(".pdf", ".txt")
                
                subprocess.call(["pdftotext", pdf_file_path, txt_file_path])
                
                txt_file = open(txt_file_path, "r")
                resume_text = txt_file.read()
                # Words that we want to parse out of the resume keywords
                stopWords = set(open(settings.ROOT + "/student/stop_words/common.txt").read().split(os.linesep))
                
                # Get rid of stop words
                fullWords = re.findall(r'[a-zA-Z]{3,}', resume_text)
                result = ""
                count = 0
                for word in fullWords:
                    word = word.lower()
                    if word not in stopWords:
                        count += 1
                        result += " " + word
    
                student.keywords = result
                student.save()
            except Exception:
                failed.append(student)
        print failed