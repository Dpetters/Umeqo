from employer.models import Employer
from django import template
from django.conf import settings
from sorl.thumbnail import get_thumbnail

register = template.Library()

''' This is cleaner but will not work until Django 1.4

@register.inclusion_tag('employer_logo.html')
def show_employer_logo(employer, *args, **kwargs):
    width = kwargs['width'] or ''
    height = kwargs['height'] or ''

    if logo and (width or height):
        dimensions = width
        if height:
            dimensions += 'x' + height
        logo = get_thumbnail(employer.logo, dimensions).url
    else:
        logo = employer.logo or None

    return {'employer': employer,
            'employer_logo': logo}'''

@register.inclusion_tag('employer_logo.html')
def show_employer_logo(employer):

    return {'employer': employer,
            'MEDIA_URL': settings.MEDIA_URL}

@register.inclusion_tag('employer_logo.html')
def show_employer_thumbnail(employer, dimensions):
    logo = employer.logo or None

    if logo:
        logo = get_thumbnail(logo, dimensions).url

    return {'employer': employer,
            'employer_logo': logo,
            'MEDIA_URL': settings.MEDIA_URL}

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
