from __future__ import division
from __future__ import absolute_import

from student import enums as student_enums
from employer.models import Employer


def student_lists_as_choices(employer_id):
    student_list_types = []
    e = Employer.objects.get(id=employer_id)
    for student_list_type in student_enums.STUDENT_LIST_TYPE_CHOICES:
        new_student_list_type = []
        student_lists = []
        if student_list_type[0] == student_enums.GENERAL:
            for student_list in student_enums.GENERAL_STUDENT_LISTS:
                student_lists.append([0, student_list[1]])
        if student_list_type[0] == student_enums.EVENT:
            for event in e.event_set.all():
                if event.type.name == "Hard Deadline" or event.type.name == "Rolling Deadline":
                    student_lists.append([event.id, event.name + " Participants"])
                else:                                        
                    student_lists.append([event.id, event.name + " RSVPs"])
                    student_lists.append([event.id, event.name + " Attendees"])
                if event.is_drop:
                    student_lists.append([event.id, event.name + " Resumebook"])
        new_student_list_type = [student_list_type[1], student_lists]
        student_list_types.append(new_student_list_type)
    return student_list_types
