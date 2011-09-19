import pyPdf, re, os, datetime

from django.conf import settings

from student.enums import RESUME_PROBLEMS


def process_resume(student):
    try:
        resume_text = ""
        resume_file = file(settings.MEDIA_ROOT + student.resume.name, "rb")
        resume = pyPdf.PdfFileReader(resume_file)
        resume.decrypt("")
        page_num = resume.getNumPages()
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
        if count > 1000*page_num:
            return RESUME_PROBLEMS.HACKED
    except Exception:
        return RESUME_PROBLEMS.HACKED
    if count == 0:
        student.keywords = result
        student.last_update = datetime.datetime.now()
        student.save()
        return RESUME_PROBLEMS.UNPARSABLE
    
    # Update the student profile and save
    student.keywords = result
    student.last_update = datetime.datetime.now()
    student.save()
    
    return