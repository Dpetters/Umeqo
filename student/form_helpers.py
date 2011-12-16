from __future__ import division
from __future__ import absolute_import

from student import enums as student_enums
from employer.models import Recruiter


def student_lists_as_choices(recruiter_id):
    student_list_types = []
    recruiter = Recruiter.objects.get(id=recruiter_id)
    e = recruiter.employer
    for student_list_type in student_enums.STUDENT_LIST_TYPE_CHOICES:
        new_student_list_type = []
        student_lists = []
        if student_list_type[0] == student_enums.GENERAL:
            for student_list in student_enums.GENERAL_STUDENT_LISTS:
                if not e.subscribed_annually() and ( student_list[1] == student_enums.GENERAL_STUDENT_LISTS[0][1] or student_list[1] == student_enums.GENERAL_STUDENT_LISTS[1][1]):
                    student_lists.append([0, student_list[1], "disabled=\"disabled\""])
                elif not e.subscribed_annually() and student_list[1] == student_enums.GENERAL_STUDENT_LISTS[2][1]:
                    student_lists.append([0, student_list[1], "selected=\"selected\""])
                else:
                    student_lists.append([0, student_list[1]])
        elif student_list_type[0] == student_enums.EVENT:
            events = e.event_set.all()
            for index, event in enumerate(events):
                if index == 0 and not e.subscribed_annually():
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " RSVPs", "selected=\"selected\""])
                else:
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " RSVPs"])
                student_lists.append([event.id, event.name.replace("\"", "\'") + " Attendees"])
                if event.is_drop:
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " Resume Drop"])
        elif student_list_type[0] == student_enums.RESUME_BOOK_HISTORY:
            rbs = recruiter.resumebook_set.filter(delivered=True)
            for rb in rbs:
                if not e.subscribed_annually():
                    student_lists.append([rb.id, rb.name, "disabled=\"disabled\""])
                else:
                    student_lists.append([rb.id, rb.name])
        new_student_list_type = [student_list_type[1], student_lists]
        student_list_types.append(new_student_list_type)
    return student_list_types
