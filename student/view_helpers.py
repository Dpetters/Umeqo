import datetime
import os
import re
import subprocess

from django.conf import settings as s

from student.enums import RESUME_PROBLEMS

def handle_uploaded_file(f, destination):
    destination = open(destination, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def process_resume(student):
    pdf_file_path = s.MEDIA_ROOT + student.resume.name
    results = resume_processing_helper(pdf_file_path)
    if results == RESUME_PROBLEMS.HACKED or results == RESUME_PROBLEMS.UNPARSABLE:
        student.keywords = ""
    else:
        student.keywords = results
    student.last_update = datetime.datetime.now()
    student.save()
    return results

def resume_processing_helper(pdf_file_path):
    try:
        txt_file_path = pdf_file_path.replace(".pdf", ".txt")
        subprocess.call(["pdftotext", pdf_file_path, txt_file_path])
        txt_file = open(txt_file_path, "r")
        resume_text = txt_file.read()
        # Words that we want to parse out of the resume keywords
        stopWords = set(open(s.ROOT + "/student/stop_words/common.txt").read().split(os.linesep))
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
        elif count == 0:
            return RESUME_PROBLEMS.UNPARSABLE
        return result
    except Exception, e:
        return RESUME_PROBLEMS.UNPARSABLE