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
        keywords = re.findall(r'[a-zA-Z0-9!-~]+', resume_text)
        num = len(keywords) + len(special_keywords_found)
        keywords = " ".join(keywords + special_keywords_found)
        
        # parse out phone numbers
        phoneNumberPattern = re.compile(r'''
                    # don't match beginning of string, number can start anywhere
        \(*         # optional parenthesis
        (\d{3})     # area code is 3 digits (e.g. '800')
        \)*         # optional closing parenthesis
        \D*         # optional separator is any number of non-digits
        (\d{3})     # trunk is 3 digits (e.g. '298')
        \D*         # optional separator
        (\d{4})     # rest of number is 4 digits (e.g. '6622')
        ''', re.VERBOSE)
        match = re.search(phoneNumberPattern, keywords)
        while match:
            keywords = keywords[:match.start()] + keywords[match.end():]
            match = re.search(phoneNumberPattern, keywords)
        
        # parse out emails
        email_re = re.compile(
        r"([-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?', re.IGNORECASE)  # domain
        match = re.search(email_re, keywords)
        while match:
            keywords = keywords[:match.start()] + keywords[match.end():]
            match = re.search(email_re, keywords)
        return keywords, num

    except Exception as e:
        return ""