import csv

from datetime import datetime, timedelta, date, time

from core.decorators import is_student, is_recruiter, is_campus_org, is_campus_org_or_recruiter
from events.choices import ALL
from events.models import Event
from haystack.query import SearchQuerySet, SQ

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

def export_event_list_csv(file_obj, event, list):
    writer = csv.writer(file_obj)
    info = ["Name", "Email", "School Year", "Graduation Year"]
    writer.writerow(info)
    if list =="rsvps":
        filename = "%s RSVPs" % (event.name)
        students = get_rsvps(event)
    elif list == "attendees":
        filename = "%s Attendees" % (event.name)
        students = get_attendees(event)
        students.sort(key=lambda n: n['name'])
    elif list == "dropped_resumes":
        filename = "%s Resume Drops" % (event.name)
        students = get_dropped_resumes(event)
        students.sort(key=lambda n: n['name'])
    elif list == "all":
        filename = "%s Respondees" % (event.name)
        students = get_all_responses(event)
        students.sort(key=lambda n: n['name'])
    for student in students:
        info = []
        info.append(student['name'])
        info.append(student['email'])
        if student['account']:
            info.append(student['school_year'])
            info.append(student['graduation_year'])
        writer.writerow(info)
    return filename

def export_event_list_text(file_obj, event, list):
    info = "\t".join(["Name", "Email", "School Year", "Graduation Year"])
    print >> file_obj, info
    if list == "all":
        filename = "%s Respondees" % (event.name)
        students = get_all_responses(event)
        students.sort(key=lambda n: n['name'])
    elif list == "rsvps":
        filename = "%s RSVPs" % (event.name)
        students = get_rsvps(event)
    elif list == "dropped_resumes":
        filename = "%s Resume Drops" % (event.name)
        students = get_dropped_resumes(event)
        students.sort(key=lambda n: n['name'])
    elif list == "attendees":
        filename = "%s Attendees" % (event.name)
        students = get_attendees(event)
        students.sort(key=lambda n: n['name'])
    for student in students:
        if student['account']:
            info = "\t".join([student['name'], student['email'], student['school_year'], student['graduation_year']])
        else:
            info = "\t".join([student['name'], student['email']])
        print >> file_obj, info
    return filename

"""
def export_event_list_xls(file_obj, event, list):
    wb = xlwt.Workbook()
    if list =="rsvps":
        worksheet_name = "%s RSVPs" % (event.name)
        students = get_rsvps(event)
    elif list == "attendees":
        worksheet_name = "%s Attendees" % (event.name)
        students = get_attendees(event)
        students.sort(key=lambda n: n['name'])
    elif list == "dropped_resumes":
        worksheet_name = "%s Resume Drop" % (event.name)
        students = get_dropped_resumes(event)
        students.sort(key=lambda n: n['name'])
    elif list == "all":
        worksheet_name = "%s All Responses" % (event.name)
        students = get_all_responses(event)
        students.sort(key=lambda n: n['name'])
    ws = wb.add_sheet(worksheet_name)
    ws.write(0, 0, 'Name')
    ws.write(0, 1, 'Email')
    ws.write(0, 2, 'School Year (Graduation Year)')
    for i, rsvp in enumerate(students, start=1):
        student = rsvp.student
        ws.write(i, 0, student['name'])
        ws.write(i, 1, student['email'])
        if student['account']:            
            ws.write(i, 2, student['school_year'])
            ws.write(i, 3, student['graduation_year'])
    wb.save(file_obj)
    return "%s.xls" % (event.name)
"""

def event_filtering_helper(category, request):
    if category=="past":
        events_sqs = get_past_events_sqs(request.user)
    elif category=="cancelled":
        events_sqs = get_cancelled_events_sqs(request.user)
    elif category=="archived":
        events_sqs = get_archived_events_sqs(request.user)
    elif category=="attended":
        events_sqs = get_attended_events_sqs(request.user)
    else:
        events_sqs = get_upcoming_events_sqs(request.user)
    
    events_exist = len(events_sqs) > 0
    
    type = request.GET.get("type", ALL)
    if type=="e":
        events_sqs = events_sqs.filter(is_deadline=False)
    elif type=="d":
        events_sqs = events_sqs.filter(is_deadline=True)        
    elif type=="r":
        events_sqs = events_sqs.filter(is_drop=True)  
    
    query = request.GET.get('query','')
    if query!="":
        for q in query.split(' '):
            if q.strip() != "":
                events_sqs = events_sqs.filter(text=q)
    
    if category =="upcoming":
        return get_categorized_events_context(events_exist, events_sqs)
    else:
        return events_exist, [sr.object for sr in events_sqs.load_all()]


def get_rsvps(event):
    return map(buildRSVP, event.rsvp_set.filter(attending=True).order_by('student__first_name'))

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

def get_attendees(event):
    attendees = map(buildAttendee, event.attendee_set.all().order_by('name'))
    return attendees

def get_dropped_resumes(event):
    return map(buildRSVP, event.droppedresume_set.all().order_by('student__first_name'))

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

def get_invitees(event):
    return map(buildRSVP, event.invitee_set.all().order_by('student__first_name'))

def get_no_rsvps(event):
    return map(buildRSVP, event.rsvp_set.filter(attending=False).order_by('student__first_name'))

def get_employer_upcoming_events_context(employer, user):
    events = SearchQuerySet().models(Event).filter(attending_employers=employer.id)
    if is_student(user):
        events = events.filter(SQ(is_public=True) | SQ(invitees=user.id))
    return get_categorized_events_context(len(events) > 0, events)

def get_user_events_sqs(user):
    events = SearchQuerySet().models(Event)
    if is_student(user):
        return events.filter(SQ(is_public=True) | SQ(invitees=user.id))
    if is_campus_org(user):
        return events.filter(owner=user.id)
    return events.filter(SQ(owner=user.id) | SQ(attending_employers=user.recruiter.employer.id))

def get_archived_events_sqs(user):
    return get_user_events_sqs(user).filter(archived=True).order_by("-end_datetime")

def get_attended_events_sqs(user):
    return get_user_events_sqs(user).filter(attendees=user.id).order_by("-end_datetime")

def get_cancelled_events_sqs(user):
    events = get_user_events_sqs(user).filter(cancelled=True).order_by("-end_datetime")
    if is_recruiter(user) or is_campus_org(user):
        events = events.filter(archived=False)
    return events

def get_past_events_sqs(user):
    events = get_user_events_sqs(user).filter(end_datetime__lt=datetime.now()).order_by("-end_datetime")
    if is_recruiter(user) or is_campus_org(user):
        events = events.filter(archived=False)
    return events

def get_categorized_events_context(events_exist, event_sqs):
    context = {'events_exist':events_exist}
    print len(event_sqs)
    tomorrow = datetime.combine(date.today() + timedelta(days=1), time())
    happening_now_events = event_sqs.filter(SQ(start_datetime__lt = datetime.now()) | SQ(type="Rolling Deadline")).order_by("end_datetime")
    later_today_events = event_sqs.filter(SQ(start_datetime__gte = datetime.now()) | SQ(end_datetime__gte = datetime.now(), type="Hard Deadline")).filter(SQ(start_datetime__lt = tomorrow) | SQ(end_datetime__lt = tomorrow, type="Hard Deadline")).order_by("start_datetime")
    tomorrows_events = event_sqs.filter(SQ(start_datetime__gte = tomorrow) | SQ(end_datetime__gte = tomorrow, type="Hard Deadline")).filter(SQ(start_datetime__lt = tomorrow + timedelta(days=1)) | SQ(end_datetime__lt = tomorrow + timedelta(days=1), type="Hard Deadline")).order_by("start_datetime")
    days_until_weeks_end = 6-date.today().weekday()
    this_week_events = event_sqs.filter(SQ(start_datetime__gte = tomorrow + timedelta(days=1)) | SQ(end_datetime__gte = tomorrow + timedelta(days=1), type="Hard Deadline")).filter(SQ(start_datetime__lt = tomorrow + timedelta(days=days_until_weeks_end)) | SQ(end_datetime__lt = tomorrow + timedelta(days=days_until_weeks_end), type="Hard Deadline")).order_by("start_datetime")
    next_week_events = event_sqs.filter(SQ(start_datetime__gte = tomorrow + timedelta(days=days_until_weeks_end)) | SQ(end_datetime__gte = tomorrow + timedelta(days=days_until_weeks_end), type="Hard Deadline")).filter(SQ(start_datetime__lt = tomorrow + timedelta(days=days_until_weeks_end+7)) | SQ(end_datetime__lt = tomorrow + timedelta(days=days_until_weeks_end+7), type="Hard Deadline")).order_by("start_datetime")
    later_events = event_sqs.filter(SQ(start_datetime__gte = tomorrow + timedelta(weeks=1)) | SQ(end_datetime__gte = tomorrow + timedelta(weeks=1), type="Hard Deadline")).order_by("start_datetime")
    context['happening_now_events'] = [sr.object for sr in happening_now_events.load_all()]
    context['later_today_events'] = [sr.object for sr in later_today_events.load_all()]
    context['tomorrows_events'] = [sr.object for sr in tomorrows_events.load_all()]
    context['this_weeks_events'] = [sr.object for sr in this_week_events.load_all()]
    context['next_weeks_events'] = [sr.object for sr in next_week_events.load_all()]
    context['later_events'] = [sr.object for sr in later_events.load_all()]
    return context
    
def get_upcoming_events_sqs(user):
    events = get_user_events_sqs(user).filter(end_datetime__gte=datetime.now())
    if is_campus_org_or_recruiter(user):
        events = events.filter(archived=False)
    return events

def get_upcoming_events_context(user):
    upcoming_events = get_upcoming_events_sqs(user)
    events_exist = False
    if len(upcoming_events) > 0:
        events_exist = True
    event_context = get_categorized_events_context(events_exist, upcoming_events)
    return event_context