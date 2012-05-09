import locale
import time

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
locale.setlocale(locale.LC_ALL, '')

@register.filter
@stringfilter
def split(str, split_token):
    return str.split(split_token)

@register.filter
def format_money(amount):
    return locale.currency(amount/100, grouping=True)

@register.filter
def format_unix_time(unix_time):
    return time.strftime("%m/%d/%Y", time.gmtime(unix_time))