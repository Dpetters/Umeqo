import pyPdf, re, os, datetime

from django.conf import settings
from django.shortcuts import redirect

def process_resume(student):
   
    resume_text = ""
    resume_file = file(settings.MEDIA_ROOT + student.resume.name, "rb")
    resume = pyPdf.PdfFileReader(resume_file)
    for i in range(0, resume.getNumPages()):
        resume_text += resume.getPage(i).extractText() + "\n"
    resume_file.close()
    
    # Words that we want to parse out of the resume keywords
    stopWords = set(open(settings.ROOT + "/student/stop_words/common.txt").read().split(os.linesep))
    
    # Get rid of stop words
    fullWords = re.findall(r'[a-zA-Z]{3,}', resume_text)
    result=""
    for word in fullWords:
        word=word.lower()
        if word not in stopWords:
            result += " " + word
    
    # Update the student profile and save
    student.keywords = result
    student.last_update = datetime.datetime.now()
    student.save()
    
    return redirect('home')