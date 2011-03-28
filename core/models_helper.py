"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
import datetime

def get_resume_filename(instance, filename): #@UnusedVariable
    filename = 'submitted_resumes/' + instance.last_name + "_" + instance.first_name + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"
    return filename

def get_image_filename(instance, filename):
    extension = filename[filename.find('.'):]
    filename = "content/images/" + instance.name.replace(" ", "_") + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + extension
    return filename