import datetime
import os
import re
import subprocess

from pyPdf import PdfFileReader

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
    if results == RESUME_PROBLEMS.FILE_PROBLEM or results == RESUME_PROBLEMS.UNPARSABLE or results == RESUME_PROBLEMS.TOO_MANY_WORDS:
        student.keywords = ""
    else:
        student.keywords = results
    student.last_update = datetime.datetime.now()
    student.save()
    return results

def resume_processing_helper(pdf_file_path):
    try:
        try:
            file = open(pdf_file_path, "rb")
            PdfFileReader(file)
            file.close()
        except Exception as e:
            return RESUME_PROBLEMS.FILE_PROBLEM
        txt_file_path = pdf_file_path.replace(".pdf", ".txt")
        subprocess.call(["pdftotext", pdf_file_path, txt_file_path])
        txt_file = open(txt_file_path, "r")
        resume_text = txt_file.read()
        
        special_terms = ["c++","c#","f#"]
        escaped_special_terms = map(re.escape, special_terms)
        re_pattern = r'(%s)+' % ("|".join(escaped_special_terms))
        special_terms_found = re.findall(re_pattern, resume_text)
        joined_special_terms_found = " ".join(special_terms_found)
        keywords = re.findall(r'[a-zA-Z0-9]+', resume_text)
        combined_keywords = " ".join(keywords)
        all_keywords = "%s %s" % (combined_keywords, joined_special_terms_found)
        if len(keywords) + len(special_terms_found) > 3000:
            return RESUME_PROBLEMS.TOO_MANY_WORDS
        elif len(keywords) == 0:
            return RESUME_PROBLEMS.UNPARSABLE
        return all_keywords
    except Exception, e:
        return RESUME_PROBLEMS.UNPARSABLE