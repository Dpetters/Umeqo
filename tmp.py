import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from events.models import Event

for e in Event.objects.all():
    checkins = []
    for i in e.attendee_set.all():
        if i.student:
            if i.student in checkins:
                print i.student 
            else:
                checkins.append(i.student)

