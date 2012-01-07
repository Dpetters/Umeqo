import datetime
import os
import re
import subprocess

from django.conf import settings

from student.enums import RESUME_PROBLEMS


def process_resume(student):
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
        if count > 2500:
            return RESUME_PROBLEMS.HACKED
    except Exception:
        return RESUME_PROBLEMS.HACKED
    
    student.keywords = result
    student.last_update = datetime.datetime.now()
    student.save()
    if count == 0:
        return RESUME_PROBLEMS.UNPARSABLE
    return