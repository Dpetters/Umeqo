from django import template
from django.conf import settings as s

register = template.Library()

@register.simple_tag
def settings_value(settings_value_id):
    return getattr(s, settings_value_id, None)
