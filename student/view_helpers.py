import re
import subprocess

from django.conf import settings as s


def handle_uploaded_file(f, destination):
    destination = open(destination, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def extract_resume_keywords(resume_file_path):
    try:
        resume_file_path = "%s%s" % (s.MEDIA_ROOT, resume_file_path)
        txt_file_path = resume_file_path.replace(".pdf", ".txt")
        subprocess.call(["pdftotext", resume_file_path, txt_file_path])
        txt_file = open(txt_file_path, "r")
        resume_text = txt_file.read()
        
        special_terms = ["c++","c#","f#"]
        escaped_special_terms = map(re.escape, special_terms)
        re_pattern = r'(%s)+' % ("|".join(escaped_special_terms))
        special_keywords_found = re.findall(re_pattern, resume_text)
        keywords = re.findall(r'[a-zA-Z0-9]+', resume_text)
        return keywords + special_keywords_found
    except Exception as e:
        return ""