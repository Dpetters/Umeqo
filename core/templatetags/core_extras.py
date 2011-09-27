from django import template
from django.utils.text import wrap

register = template.Library()

@register.filter(name='wordwrapwithindent')
@template.defaultfilters.stringfilter
def wordwrapwithindent(value, arg):
    lines = wrap(value, int(arg)).split('\n')
    return '    ' + '\n    '.join(lines)
wordwrapwithindent.is_safe = True

@register.filter(name='stripspaces')
@template.defaultfilters.stringfilter
def stripspaces(value):
    return value.strip()
wordwrapwithindent.is_safe = True
