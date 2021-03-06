from __future__ import division
from __future__ import absolute_import

def enum(**enums):
    return type('Enum', (), enums)

RESUME_PROBLEMS = enum(TOO_MANY_WORDS = 1, UNPARSABLE = 2, FILE_PROBLEM = 3)

GENERAL = 0
EVENT = 2
RESUME_BOOK_HISTORY = 3

STUDENT_LIST_TYPE_CHOICES = (
    (GENERAL, 'General'),
    (EVENT, 'Events'),
    (RESUME_BOOK_HISTORY, 'Past Resume Books')
)

ALL_STUDENTS = 0
UNLOCKED_STUDENTS = 3
STARRED_STUDENTS = 1
STUDENTS_IN_RESUME_BOOK = 2

GENERAL_STUDENT_LISTS = (
    (ALL_STUDENTS, "All Students"),
#    (UNLOCKED_STUDENTS, "Unlocked Students"),
    (STARRED_STUDENTS, "Starred Students"),
    (STUDENTS_IN_RESUME_BOOK , "Students In Current Resume Book"),
)
