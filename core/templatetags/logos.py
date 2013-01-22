from django import template
from django.conf import settings
from sorl.thumbnail import get_thumbnail

register = template.Library()


@register.inclusion_tag('course_image.html')
def show_course_thumbnail(course, dimensions):
    course_image = course.image or None
    if course_image:
        course_image = get_thumbnail(course_image, dimensions).url

    return {'course': course,
            'course_image': course_image,
            'MEDIA_URL': settings.MEDIA_URL}

@register.inclusion_tag('employer_logo.html')
def show_employer_thumbnail(user, employer, dimensions):
    context = {}
    context["user"] = user
    if employer:
        context['employer'] = employer
        if employer.logo:
            context['logo'] = get_thumbnail(employer.logo, dimensions).url
            context['MEDIA_URL'] = settings.MEDIA_URL
    return context

@register.inclusion_tag('campus_org_logo.html')
def show_campusorg_logo(campusorg):

    return {'campus_org': campusorg,
            'MEDIA_URL': settings.MEDIA_URL}

@register.inclusion_tag('campus_org_logo.html')
def show_campusorg_thumbnail(campusorg, dimensions):
    logo = campusorg.image or None

    if logo:
        logo = get_thumbnail(logo, dimensions).url

    return {'campus_org': campusorg,
            'campus_org_logo': logo,
            'MEDIA_URL': settings.MEDIA_URL}
