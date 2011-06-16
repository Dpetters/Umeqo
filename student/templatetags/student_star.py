from django import template

register = template.Library()

@register.inclusion_tag('student_star.html')
def student_star(starred):
    return {'starred': starred}