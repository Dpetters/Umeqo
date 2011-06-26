import pyPdf, re, os, datetime

from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

def process_resume(student, ajax):
   
    resume_text = ""
    resume_file = file(student.resume.name, "rb")
    resume = pyPdf.PdfFileReader(resume_file)
    for i in range(0, resume.getNumPages()):
        resume_text += resume.getPage(i).extractText() + "\n"
    resume_file.close()
    
    # Words that we want to parse out of the resume keywords
    stopWords = set(open(settings.ROOT + "/student/stop_words/common.txt").read().split(os.linesep))
    
    # Get rid of stop words
    fullWords = re.findall(r'[a-zA-Z]{3,}', resume_text)
    result = ""
    for word in fullWords:
        word = word.lower()
        if word not in stopWords:
            result += " " + word
    
    # Update the student profile and save
    student.keywords = result
    student.last_update = datetime.datetime.now()
    student.save()
    
    if ajax:
        data = {'valid':True,
                'success_url':reverse("home")}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    return redirect(reverse('home') + '?msg=profile_saved')
