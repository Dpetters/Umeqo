from django import template
from core import messages
register = template.Library()

@register.simple_tag
def text_snippet(text_snippet_id):
    return getattr(messages, text_snippet_id)