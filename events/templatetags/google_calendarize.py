from datetime import timedelta
from django import template
from django.contrib.sites.models import Site
from django.utils.http import urlquote_plus

register = template.Library()
"""
@register.filter
def google_calendarize(event):
    
    name = urlquote_plus(event.name)
    description = urlquote_plus(event.description)
    
    st = event.datetime
    if event.type.name != "Deadline":
        length = timedelta(days = event.days or 0, hours = event.hours or 0, minutes = event.minutes or 0)
        en = event.datetime + length
    else:
        en = event.datetime
    tfmt = '%Y%m%dT%H%M%S'
    
    dates = '%s%s%s' % (st.strftime(tfmt), '%2F', en.strftime(tfmt))
    
    s = ('http://www.google.com/calendar/event?action=TEMPLATE&' +
         'text=' + name + '&' +
         'dates=' + dates + '&' +
         'details=' + description + '&' +
         'sprop=website:' + urlquote_plus(Site.objects.get_current().domain))

    if event.location:
        s = s + '&location=' + urlquote_plus(event.location)

    return s + '&trp=false'

google_calendarize.safe = True
"""