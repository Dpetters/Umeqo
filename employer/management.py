"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from employer.models import Employer
from student.models import StudentList
from student import enums as student_enums
from student import constants as student_constants

@receiver(post_save, sender=Employer)
def employer_creation_callback(instance, **kwargs):
    print "YAHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    latest_student_matches = StudentList(name=student_constants.LATEST_DEFAULT_FILTERING_STUDENT_GROUP_NAME, type=student_enums.GENERAL)
    latest_student_matches.employers.add(kwargs.get("instance", ""))
    all_student_matches = StudentList(name=student_constants.ALL_DEFAULT_FILTERING_STUDENT_GROUP_NAME, type=student_enums.GENERAL)
    all_student_matches.employers.add(kwargs.get("instance", ""))
    in_current_resume_book = StudentList(name=student_constants.IN_CURRENT_RESUME_BOOK_STUDENT_GROUP_NAME, type=student_enums.GENERAL)
    in_current_resume_book.employers.add(kwargs.get("instance", ""))  