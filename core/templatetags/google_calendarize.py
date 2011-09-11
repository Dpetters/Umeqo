from django import template
from django.contrib.sites.models import Site
from django.utils.http import urlquote_plus

register = template.Library()

register = template.Library()

@register.filter
def google_calendarize(event):
    
    name = urlquote_plus(event.name)
    
    tfmt = '%Y%m%dT%H%M%S'
    
    start_datetime = event.start_datetime
    end_datetime = event.end_datetime
    
    if not start_datetime:
        start_datetime = end_datetime
    dates = '%s%s%s' % (start_datetime.strftime(tfmt), '%2F', end_datetime.strftime(tfmt))
    
    s = ('http://www.google.com/calendar/event?action=TEMPLATE&' +
         'text=' + name + '&' +
         'dates=' + dates + '&' +
         'sprop=website:' + urlquote_plus(Site.objects.get_current().domain))

    if event.location:
        s = s + '&location=' + urlquote_plus(event.location)

    return s + '&trp=false'

google_calendarize.safe = True