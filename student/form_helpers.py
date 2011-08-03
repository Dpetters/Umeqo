from student import enums as student_enums
from events.models import Event
from employer.models import Employer


def student_lists_as_choices(employer_id):
    print employer_id
    student_list_types = []
    for student_list_type in student_enums.STUDENT_LIST_TYPE_CHOICES:
        new_student_list_type = []
        student_lists = []
        if student_list_type[0] == student_enums.GENERAL:
            for student_list in student_enums.GENERAL_STUDENT_LISTS:
                student_lists.append([0, student_list[1]])
        if student_list_type[0] == student_enums.EVENT:
            for event in Event.objects.filter(owner__in = [recruiter.user for recruiter in Employer.objects.get(id=employer_id).recruiter_set.all()]):
                student_lists.append([0, event.name + " RSVPS"])
                student_lists.append([0, event.name + " Attendees"])
        new_student_list_type = [student_list_type[1], student_lists]
        student_list_types.append(new_student_list_type)
    return student_list_types
