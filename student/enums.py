"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""


GENERAL = 0
EVENT = 2

STUDENT_LIST_TYPE_CHOICES = (
    (GENERAL, 'General'),
    (EVENT, 'Event')
)


ALL_STUDENTS = 0
STARRED_STUDENTS = 1
STUDENTS_IN_RESUME_BOOK = 2
LATEST_DEFAULT_FILTERING_PARAMETER_MATCHES = 3
ALL_DEFAULT_FILTERING_PARAMETER_MATCHES = 4

GENERAL_STUDENT_LISTS = (
    (ALL_STUDENTS, "All Students"),
    (STARRED_STUDENTS, "Starred Students"),
    (STUDENTS_IN_RESUME_BOOK , "Students In Resume Book"),
    (LATEST_DEFAULT_FILTERING_PARAMETER_MATCHES, "Latest Default Filtering Parameter Matches"),
    (ALL_DEFAULT_FILTERING_PARAMETER_MATCHES, "All Default Filtering Parameter Matches")
)