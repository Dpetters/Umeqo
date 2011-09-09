from django import template
from django.contrib.sites.models import Site
from django.utils.http import urlquote_plus
from django.utils.html import strip_tags

register = template.Library()

register = template.Library()

@register.filter
def google_calendarize(event):
    
    name = urlquote_plus(event.name)
    description = urlquote_plus(strip_tags(event.description))
    
    tfmt = '%Y%m%dT%H%M%S'
    dates = '%s%s%s' % (event.start_datetime.strftime(tfmt), '%2F', event.end_datetime.strftime(tfmt))
    
    s = ('http://www.google.com/calendar/event?action=TEMPLATE&' +
         'text=' + name + '&' +
         'dates=' + dates + '&' +
         'details=' + strip_tags(description) + '&' +
         'sprop=website:' + urlquote_plus(Site.objects.get_current().domain))

    if event.location:
        s = s + '&location=' + urlquote_plus(event.location)

    return s + '&trp=false'

google_calendarize.safe = True