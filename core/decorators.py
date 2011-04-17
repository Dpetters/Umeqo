"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from student.models import Student
from employer.models import Employer

def is_student(user):
    try:
        user.student
    except Student.DoesNotExist:
        return False
    return True
    
def is_employer(user):
    try:
        user.employer
    except Employer.DoesNotExist:
        return False
    return True