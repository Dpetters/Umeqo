import csv

from datetime import datetime, timedelta

from core.decorators import is_student
from events.models import Event
from haystack.query import SearchQuerySet

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

def get_dropped_resumes(event):
    return map(buildRSVP, event.droppedresume_set.all().order_by('student__first_name'))
    
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
