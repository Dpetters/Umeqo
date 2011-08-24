from datetime import datetime
from events.models import Event
from haystack.query import SearchQuerySet

def event_search_helper(request):
    query = request.GET.get('q','')
    search_results = SearchQuerySet().models(Event).filter(is_public=True).filter(end_datetime__gte=datetime.now()).order_by("start_datetime")
    if query!="":
        for q in query.split(' '):
            if q.strip() != "":
                search_results = search_results.filter(content_auto=q)
    return map(lambda n: n.object, search_results)

def event_page_redirect(request, id):
    event = Event.objects.get(pk=id)
    return redirect(event.get_absolute_url())

def buildAttendee(obj):
    output = {
        'email': obj.email,
        'datetime_created': obj.datetime_created.isoformat()
    }
    if obj.student:
        output['name'] = obj.student.first_name + ' ' + obj.student.last_name
        output['account'] = True
        output['id'] = obj.student.id
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
        'account': True
    }
    return output

def get_event_schedule(event_date_string):
    event_date = datetime.strptime(event_date_string, '%m/%d/%Y')
    event_date_tmrw = event_date + timedelta(days=1)
    events = Event.objects.all().filter(start_datetime__gt=event_date).filter(start_datetime__lt=event_date_tmrw)
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