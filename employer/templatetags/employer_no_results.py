from django import template
from student import enums as student_enums
register = template.Library()

@register.inclusion_tag('employer_no_results.html')
def employer_no_results(current_student_list, filtering):
    context = {}
    context['filtering'] = filtering
    context['current_student_list'] = current_student_list
    #context['unlocked_students_student_list'] = student_enums.GENERAL_STUDENT_LISTS[1][1]
    context['in_resume_book_student_list'] = student_enums.GENERAL_STUDENT_LISTS[2][1]
    context['all_students'] = student_enums.GENERAL_STUDENT_LISTS[0][1]
    context['starred_students'] = student_enums.GENERAL_STUDENT_LISTS[1][1]
    parts = current_student_list.split(" ")
    if parts[-1] == "RSVPs" or parts[-1] == "Attendees":
        context['type'] = parts[-1]
    elif parts[-1] == "Drop" and parts[-2] == "Resume":
        context['type'] = "Resume Drop"
    return context
