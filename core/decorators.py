"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.conf import  settings

def is_student(user):
    if user:
        return user.groups.filter(name=settings.STUDENT_GROUP_NAME).count() > 0
    return False

def is_employer(user):
    if user:
        return user.groups.filter(name=settings.EMPLOYER_GROUP_NAME).count() > 0
    return False