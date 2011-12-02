from datetime import datetime, timedelta

from django.db.models import Q

from core.decorators import is_student
from events.models import Event
from haystack.query import SearchQuerySet
            
def event_search_helper(request):
    query = request.GET.get('q','')
    if is_student(request.user):
        search_results = SearchQuerySet().models(Event).filter(is_public=True).filter(end_datetime__gte=datetime.now()).order_by("end_datetime")
    if query!="":
        for q in query.split(' '):
            if q.strip() != "":
                search_results = search_results.filter(content_auto=q)
    return map(lambda n: n.object, search_results)

def get_rsvps(event):
    return map(buildRSVP, event.rsvp_set.filter(attending=True).order_by('student__first_name'))

def get_no_rsvps(event):
    return map(buildRSVP, event.rsvp_set.filter(attending=False).order_by('student__first_name'))

def get_attendees(event):
    attendees = map(buildAttendee, event.attendee_set.all().order_by('name'))
    return attendees

def get_invitees(event):
    return map(buildRSVP, event.invitee_set.all().order_by('student__first_name'))
    
def get_all_responses(event):
    all_responses = []
    emails_dict = {}
    students = []
    attendees = get_attendees(event)
    if attendees:
        students.extend(attendees)
    rsvps = get_rsvps(event)
    if rsvps:
        students.extend(rsvps)
    no_rsvps = get_no_rsvps(event)
    if no_rsvps:
        students.extend(no_rsvps) 
    for res in students:
        if res['email'] not in emails_dict:
            emails_dict[res['email']] = 1
            all_responses.append(res)
    all_responses.sort(key=lambda n: n['name'])
    return all_responses

def buildAttendee(obj):
    output = {
        'email': obj.email,
        'datetime_created': obj.datetime_created.isoformat()
    }
    if obj.student and obj.student.profile_created:
            output['name'] = obj.student.first_name + ' ' + obj.student.last_name
            output['account'] = True
            output['id'] = obj.student.id
            output['school_year'] = str(obj.student.school_year)
            output['graduation_year'] = str(obj.student.graduation_year)
    else:
        output['name'] = obj.name
        output['account'] = False
    return output

def buildRSVP(obj):
    output = {
        'id': obj.student.id,
        'name': obj.student.first_name + ' ' + obj.student.last_name,
        'datetime_created': obj.datetime_created.isoformat(),
        'email': obj.student.user.email,
        'school_year': str(obj.student.school_year),
        'graduation_year': str(obj.student.graduation_year),
        'account': True
    }
    return output

def get_event_schedule(event_date_string, event_id):
    event_date = datetime.strptime(event_date_string, '%m/%d/%Y')
    event_date_tmrw = event_date + timedelta(days=1)
    events = Event.objects.all().filter(start_datetime__gt=event_date).filter(start_datetime__lt=event_date_tmrw)
    if event_id:
        event_id = int(event_id)
        events = events.exclude(id=event_id)
    def buildScheduleItem(event):
        name = event.name
        start = event.start_datetime
        start_hour = start.hour + start.minute/60.0
        end = event.end_datetime
        if event.end_datetime > event_date_tmrw:
            end_hour = 24
        else:
            end_hour = end.hour + end.minute/60.0
        start_px, end_px = map(lambda t: int(1 + 32*t), (start_hour, end_hour))
        return name, start_px, (end_px - start_px)
    schedule = map(buildScheduleItem, events)
    return schedule
