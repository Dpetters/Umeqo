from django import template

register = template.Library()

@register.inclusion_tag('student_resume_book.html')
def student_resume_book(in_resume_book):
    return {'in_resume_book': in_resume_book}