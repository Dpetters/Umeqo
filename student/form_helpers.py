"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from student import enums as student_enums


def student_lists_as_choices(employer):
    student_list_types = []
    for student_list_type in student_enums.STUDENT_GROUP_TYPE_CHOICES:
        new_student_list_type = []
        student_lists = []
        print student_list_type
        for student_list in employer.studentlist_set.filter(type=student_list_type[0]):
            student_lists.append([student_list.id, student_list.name])
        
        new_student_list_type = [student_list_type[1], student_lists]
        student_list_types.append(new_student_list_type)
    print student_list_types
    return student_list_types
