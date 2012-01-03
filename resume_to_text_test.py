import pyPdf, re, os

from django.conf import settings

from student.models import Student

def convert_resume():
    output = open("output", "w")
    student = Student.objects.get(id=5)
    print settings.MEDIA_ROOT + student.resume.name
    resume_file = file(settings.MEDIA_ROOT + student.resume.name, "rb")
    resume = pyPdf.PdfFileReader(resume_file)
    if resume.getIsEncrypted():
        resume.decrypt("")
    page_num = resume.getNumPages()
    resume_text = ""
    for i in range(0, page_num):
        resume_text += resume.getPage(i).extractText() + "\n"

    resume_file.close()
    
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
            
    output.write(result)
    output.close()