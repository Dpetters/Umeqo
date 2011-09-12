from django import template
from student import enums as student_enums
register = template.Library()

@register.inclusion_tag('employer_no_results.html')
def employer_no_results(current_student_list, filtering):
    context = {}
    context['filtering'] = filtering
    context['current_student_list'] = current_student_list
    context['in_resume_book_student_list'] = student_enums.GENERAL_STUDENT_LISTS[2][1]
    context['all_students'] = student_enums.GENERAL_STUDENT_LISTS[0][1]
    context['starred_students'] = student_enums.GENERAL_STUDENT_LISTS[1][1]
    type = current_student_list.split(" ")[-1]
    if type == "RSVPs" or type == "Attendees" or type=="Resumebook":
        context['type'] = type
    return context