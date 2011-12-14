from __future__ import division
from __future__ import absolute_import

import csv
import cStringIO as StringIO
from datetime import datetime, timedelta
import re
import xlwt

from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, Http404
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.shortcuts import redirect, render_to_response
from django.template.loader import render_to_string

from campus_org.models import CampusOrg
from employer.models import Employer
from core.email import send_html_mail
from core import enums as core_enums
from core.decorators import agreed_to_terms, is_recruiter, is_student, is_campus_org_or_recruiter, is_campus_org, render_to, has_annual_subscription, has_any_subscription
from core.models import Edit
from core.view_helpers import english_join
from events.forms import EventForm, CampusOrgEventForm, EventExportForm
from events.models import notify_about_event, Attendee, Event, EventType, Invitee, RSVP, DroppedResume
from events.view_helpers import event_search_helper, get_event_schedule, get_attendees, get_invitees, get_rsvps, get_no_rsvps, get_all_responses
from notification import models as notification
from student.models import Student

@require_GET
@agreed_to_terms
def events_shortcut(request, owner_slug, event_slug, extra_context=None):
    try:
        employer = Employer.objects.get(slug = owner_slug)
        print employer
        events = reduce(lambda a,b: [a, a.extend(b.user.event_set.all().order_by("-date_created"))][0], employer.recruiter_set.all(), [])
    except Employer.DoesNotExist:
        try:
            campus_org = CampusOrg.objects.get(slug = owner_slug)
            print campus_org
            events = campus_org.user.event_set.all().order_by("-date_created")
        except CampusOrg.DoesNotExist:
            raise Http404
    if events != []:
        try:
            slug_matches = filter(lambda a: a.short_slug == event_slug, events)
            if slug_matches:
                url = slug_matches[0].get_absolute_url()
                if url:
                    return redirect(url)
        except Event.DoesNotExist:
            pass
    raise Http404

@login_required
@agreed_to_terms
@user_passes_test(is_student)
@render_to('events_list.html')
def events_list(request, extra_context=None):
    if not request.user.student.profile_created:
        return redirect('student_profile')
    query = request.GET.get('q', '')
    events = event_search_helper(request)
    context = {
        'events': events,
        'query': query
    }
    context.update(extra_context or {})
    return context

def event_page_redirect(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        raise Http404
    return redirect("%s" % (event.get_absolute_url()))

@render_to('event_page.html')
@agreed_to_terms
def event_page(request, id, slug, extra_context=None):
    if is_student(request.user) and not request.user.student.profile_created:
        return redirect('student_profile')

    if not Event.objects.filter(pk=id).exists():
        raise Http404
    event = Event.objects.get(pk=id)

    if not event.is_public:
        if not request.user.is_authenticated():
            return HttpResponseForbidden("You don't have permission to view this event.")
        elif is_campus_org(request.user):
            if request.user != event.owner:
                return HttpResponseForbidden("You don't have permission to view this event.")
        elif is_recruiter(request.user):
            if request.user.recruiter.employer not in event.attending_employers.all():
                return HttpResponseForbidden("You don't have permission to view this event.")
        elif is_student(request.user):
            try:
                Invitee.objects.get(event=event, student=request.user.student)
            except:
                return HttpResponseForbidden("You don't have permission to view this event.")

    current_site = Site.objects.get(id=s.SITE_ID)

    page_url = 'http://' + current_site.domain + event.get_absolute_url()
    #google_description is the description + stuff to link back to umeqo
    google_description = event.description + '\n\nRSVP and more at %s' % page_url
    
    context = {
        'event': event,
        'invitees': get_invitees(event),
        'rsvps': get_rsvps(event),
        'no_rsvps': get_no_rsvps(event),
        'attendees': get_attendees(event),
        'all_responses': get_all_responses(event),
        'page_url': page_url,
        'DOMAIN': current_site.domain,
        'current_site':"http://" + current_site.domain,
        'is_deadline': (event.type == EventType.objects.get(name='Hard Deadline') or event.type == EventType.objects.get(name='Rolling Deadline')),
        'google_description': google_description
    }
    if event.end_datetime:
        context['is_past'] = event.end_datetime < datetime.now()
        
    if len(event.audience.all()) > 0:
        context['audience'] = event.audience.all()
    
    if is_campus_org(event.owner):
        context['campus_org_event'] = True
        context['attending_employers'] = event.attending_employers
        if is_campus_org(request.user):
            context['resume_drops'] = len(event.droppedresume_set.all())
            context['can_edit'] = (event.owner == request.user)
            context['show_admin'] = (event.owner == request.user)
        elif is_recruiter(request.user):
            context['resume_drops'] = len(event.droppedresume_set.all())
            context['show_admin'] = request.user.recruiter.employer in event.attending_employers.all()
    elif is_recruiter(event.owner):
        if is_recruiter(request.user):
            context['can_edit'] = request.user.recruiter in event.owner.recruiter.employer.recruiter_set.all() and request.user.recruiter.employer.subscribed()
            context['show_admin'] = request.user.recruiter in event.owner.recruiter.employer.recruiter_set.all() and request.user.recruiter.employer.subscribed()
            context['resume_drops'] = len(event.droppedresume_set.all())
    if not is_campus_org(request.user) and not is_recruiter(request.user):
        event.view_count += 1
        event.save()
            
    if is_student(request.user):
        
        rsvp = RSVP.objects.filter(event=event, student=request.user.student)
        print rsvp
        if rsvp.exists():
            context['attending'] = rsvp.get().attending
            context['responded'] = True
        
        dropped_resume = DroppedResume.objects.filter(event=event, student=request.user.student)
        if dropped_resume.exists():
            context['dropped_resume'] = True
        
        context['can_rsvp'] = True
    else:
        context['email_delivery_type'] = core_enums.EMAIL
    context.update(extra_context or {})
    return context

@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@agreed_to_terms
@render_to("event_form.html")
def event_new(request, form_class=None, extra_context=None):
    context = {}
    if is_recruiter(request.user):
        employer = request.user.recruiter.employer
        form_class = EventForm
    elif is_campus_org(request.user):
        form_class = CampusOrgEventForm
        context['max_industries'] = s.EP_MAX_INDUSTRIES
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            form.save_m2m()
            rolling_deadline = EventType.objects.get(name="Rolling Deadline")
            if event.type == rolling_deadline:
                event.end_datetime = datetime.now() + timedelta(weeks=1000)
                event.save()
            if is_recruiter(request.user):
                event.attending_employers.add(employer);
                # Update index
                employer.save();
            notify_about_event(event, "new_event", event.attending_employers.all())
            return HttpResponseRedirect(reverse('event_page', kwargs={'id':event.id, 'slug':event.slug}))
    else:
        form = form_class(initial={
            'start_datetime': datetime.now() + timedelta(minutes=30),
            'end_datetime': datetime.now() + timedelta(hours=1, minutes=30),
        })
    context['hours'] = map(lambda x,y: str(x) + y, [12] + range(1,13) + range(1,12), ['am']*12 + ['pm']*12)
    context['form'] = form
    context['today'] = datetime.now().strftime('%m/%d/%Y')
    context['event_scheduler_date'] = datetime.now().strftime('%m/%d/%Y')
    context.update(extra_context or {})
    return context

def export_event_list_csv(file_obj, event, list):
    writer = csv.writer(file_obj)
    info = ["Name", "Email", "School Year", "Graduation Year"]
    writer.writerow(info)
    if list =="rsvps":
        filename = "%s RSVPs.csv" % (event.name)
        students = get_rsvps(event)
    elif list == "attendees":
        filename = "%s Attendees.csv" % (event.name)
        students = get_attendees(event)
        students.sort(key=lambda n: n['name'])
    elif list == "all":
        filename = "%s All Responses.csv" % (event.name)
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

# Not used currently because Amazon SES doesn't support excel attachements
def export_event_list_xls(file_obj, event, list):
    wb = xlwt.Workbook()
    if list =="rsvps":
        worksheet_name = "%s RSVPs" % (event.name)
        students = get_rsvps(event)
    elif list == "attendees":
        worksheet_name = "%s Attendees" % (event.name)
        students = get_attendees(event)
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

def export_event_list_text(file_obj, event, list):
    info = "\t".join(["Name", "Email", "School Year", "Graduation Year"])
    print >> file_obj, info
    if list == "all":
        filename = "%s All Responses.txt" % (event.name)
        students = get_all_responses(event)
        students.sort(key=lambda n: n['name'])
    if list == "rsvps":
        filename = "%s RSVPs.txt" % (event.name)
        students = get_rsvps(event)
    elif list == "attendees":
        filename = "%s Attendees.txt" % (event.name)
        students = get_attendees(event)
        students.sort(key=lambda n: n['name'])
    for student in students:
        if student['account']:
            info = "\t".join([student['name'], student['email'], student['school_year'], student['graduation_year']])
        else:
            info = "\t".join([student['name'], student['email']])
        print >> file_obj, info
    return filename

@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
def event_list_download(request):
    event = Event.objects.get(id=request.GET["event_id"])
    list = request.GET['event_list']
    if request.GET['export_format'] == core_enums.CSV:
        response = HttpResponse(mimetype='text/csv')
        filename = export_event_list_csv(response, event, list)
    elif request.GET['export_format'] == core_enums.XLS:
        response = HttpResponse(mimetype="application/ms-excel")
        filename = export_event_list_xls(response, event, list)
    elif request.GET['export_format'] == core_enums.TEXT:
        response = HttpResponse(mimetype="text/plain")
        filename = export_event_list_text(response, event, list)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
def event_checkin_count(request):
    data = {'count':len(Event.objects.get(id=request.GET["event_id"]).attendee_set.all())}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    

@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@render_to('event_list_export_completed.html')
def event_list_export_completed(request, extra_context = None):
    context = {'list':request.GET['list']}
    context.update(extra_context or {})
    return context


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@render_to()
def event_list_export(request, form_class = EventExportForm, extra_context=None):
    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST)
            if form.is_valid():
                format = form.cleaned_data["export_format"]
                event = Event.objects.get(id=form.cleaned_data["event_id"])
                list = form.cleaned_data['event_list']
                
                reg = re.compile(r"\s*[;, \n]\s*")
                recipients = reg.split(request.POST['emails'])
                
                subject = ''.join(render_to_string('event_list_export_email_subject.txt', {}).splitlines())

                body = render_to_string('event_list_export_email_body.html', {'name':request.user.first_name})

                file = StringIO.StringIO()
                if format == core_enums.CSV:
                    filename = export_event_list_csv(file, event, list)
                    file_contents = file.getvalue()
                    send_html_mail(subject, body, recipients, "%s" % (filename), file_contents, "text/csv")
                elif format == core_enums.XLS:
                    filename = export_event_list_xls(file, event, list)
                    file_contents = file.getvalue()
                    send_html_mail(subject, body, recipients, "%s" % (filename), file_contents, "application/vnd.ms-excel")
                elif format == core_enums.TEXT:
                    filename = export_event_list_text(file, event, list)
                    file_contents = file.getvalue()
                    send_html_mail(subject, body, recipients, "%s" % (filename), file_contents, "text/plain")

                context = {'list': list, 'TEMPLATE':'event_list_export_completed.html'}
                context.update(extra_context or {})
                return context
            else:
                data = {'errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            form = form_class(initial={'emails':request.user.email, 'event_id':request.GET['event_id'], 'event_list':request.GET['event_list']})
        context = {'form': form, 'TEMPLATE':'event_list_export.html'}
        context.update(extra_context or {}) 
        return context
    else:
        raise HttpResponseForbidden()


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@render_to("event_form.html")
def event_edit(request, id=None, extra_context=None):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        raise Http404
    context = {}
    context['event'] = event
    if is_recruiter(event.owner):
        form_class = EventForm
        if not is_recruiter(request.user) or request.user.recruiter.employer != event.owner.recruiter.employer:
            return HttpResponseForbidden('You are not allowed to edit this event.')                
    elif is_campus_org(event.owner):
        context['max_industries'] = s.EP_MAX_INDUSTRIES
        context['attending_employers'] = event.attending_employers
        form_class = CampusOrgEventForm
        if not is_campus_org(request.user) or request.user.campusorg != event.owner.campusorg:
            return HttpResponseForbidden('You are not allowed to edit this event.') 
    if request.method == 'POST':
        attending_employers_before = list(event.attending_employers.all())[:]
        form = form_class(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.edits.add(Edit.objects.create(user=request.user))
            event.save()
            form.save_m2m()
            notify_about_event(event, "new_event", [e for e in list(event.attending_employers.all()) if e not in list(attending_employers_before)])
            return HttpResponseRedirect(reverse('event_page', kwargs={'id':event.id, 'slug':event.slug}))
    else:
        form = form_class(instance=event)
    context['edit'] = True
    context['hours'] = map(lambda x,y: str(x) + y, [12] + range(1,13) + range(1,12), ['am']*12 + ['pm']*12)
    context['form'] = form
    context['today'] = datetime.now().strftime('%m/%d/%Y')
    if event.type.name == "Hard Deadline":
        context['event_scheduler_date'] = event.end_datetime.strftime('%m/%d/%Y')
    elif event.type.name == "Rolling Deadline":
        context['event_scheduler_date'] = datetime.now().strftime('%m/%d/%Y')
    else:
        context['event_scheduler_date'] =  event.start_datetime.strftime('%m/%d/%Y')
    context.update(extra_context or {})
    return context

@login_required
@agreed_to_terms
@has_annual_subscription
@user_passes_test(is_campus_org_or_recruiter)
def event_end(request, id, extra_context = None):
    if request.is_ajax():
        try:
            event = Event.objects.get(pk=id)
        except Event.DoesNotExist:
            return HttpResponseNotFound("Event with id %s not found." % id)
        else:
            if not event.is_rolling_deadline():
                return HttpResponseForbidden('You cannot end anything other than a rolling deadline.')
            if is_recruiter(event.owner):
                if not is_recruiter(request.user) or request.user.recruiter.employer != event.owner.recruiter.employer:
                    return HttpResponseForbidden('You are not allowed to end this rolling deadline.')
            elif is_campus_org(event.owner):
                if not is_campus_org(request.user) or request.user.campusorg != event.owner.campusorg:
                    return HttpResponseForbidden('You are not allowed to end this rolling deadline.')
            event.end_date = datetime.now()
            event.save()
            return HttpResponse()
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@agreed_to_terms
@has_annual_subscription
@user_passes_test(is_campus_org_or_recruiter)
@render_to("event_cancel_dialog.html")
def event_cancel(request, extra_context = None):
    if request.is_ajax():
        if request.method == "POST":
            event_id = request.POST.get("event_id")
            if not event_id:
                return HttpResponseBadRequest("Request is missing event id.")
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return HttpResponseNotFound("Event with id %s not found." % event_id)
            else:
                if is_recruiter(event.owner):
                    if not is_recruiter(request.user) or request.user.recruiter.employer != event.owner.recruiter.employer:
                        return HttpResponseForbidden('You are not allowed to delete this event.')
                elif is_campus_org(event.owner):
                    if not is_campus_org(request.user) or request.user.campusorg != event.owner.campusorg:
                        return HttpResponseForbidden('You are not allowed to delete this event.')
                event.is_active = False
    
                # Notify RSVPS.
                rsvps = map(lambda n: n.student.user, event.rsvp_set.all())
                employers = event.attending_employers.all()
                has_word = "has" if len(employers)==1 else "have"
                employer_names = english_join(map(lambda n: n.name, employers))
                notification.send(rsvps, 'cancelled_event', {
                    'employer_names': employer_names,
                    'has_word': has_word,
                    'event': event
                })
                
                event.save()
                
                data = {}
                if event.is_deadline():
                    data['type'] = "deadline"
                else:
                    data['type'] = "event"
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            event_id = request.GET.get("event_id")
            if not event_id:
                return HttpResponseBadRequest("Request is missing event id.")
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return HttpResponseNotFound("Event with id %s not found." % event_id)
            context = {'event':event}
            context.update(extra_context or {})
            return context
    else:
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest") 


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
def event_schedule(request):
    if request.is_ajax():
        schedule = get_event_schedule(request.GET.get('event_date', datetime.now().strftime('%m/%d/%Y')), request.GET.get('event_id', None))
        return HttpResponse(simplejson.dumps(schedule), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
@agreed_to_terms
@require_http_methods(["GET", "POST"])
@has_any_subscription
def event_rsvp(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except:
        return HttpResponseBadRequest("An event with the id %d does not exist." % event_id)
    else:
        # if method is GET then get a list of RSVPed students
        if request.method == 'GET' and is_campus_org_or_recruiter(request.user):
            data = map(lambda n: {'id': n.student.id, 'email': n.student.user.email}, event.rsvp_set.all())
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        # if POST then record student's RSVP
        elif request.method == 'POST' and is_student(request.user):
            isAttending = request.POST.get('attending', 'true')
            isAttending = True if isAttending=='true' else False
            rsvp, created = RSVP.objects.get_or_create(student=request.user.student, event=event)
            rsvp.attending = isAttending
            rsvp.save()
            print rsvp
            if isAttending:
                DroppedResume.objects.get_or_create(event=event, student=request.user.student)
            if request.is_ajax():
                return HttpResponse()
            else:
                return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))
        else:
            return HttpResponseForbidden("You do not have access to this view.")

@login_required
@agreed_to_terms
@user_passes_test(is_student)
@require_POST
def event_drop(request, event_id):
    if not event_id:
        return HttpResponseBadRequest("Event id is missing.")
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseBadRequest("Event with id %d does not exist." % event_id)
    if  not request.POST.has_key("drop"):
        return HttpResponseBadRequest("Request post is missing a 'drop' boolean.")
    if request.POST["drop"]=="true":
        DroppedResume.objects.get_or_create(event=event, student=request.user.student)
    else:
        DroppedResume.objects.filter(event=event, student=request.user.student).delete()
    return HttpResponse()

@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@require_GET
def event_raffle_winner(request, extra_context=None):
    if request.is_ajax():
        if request.GET.has_key("event_id"):
            data = {}
            winners = Attendee.objects.filter(event__id=request.GET['event_id'], won_raffle=False)
            if winners.exists():
                winner = winners[0]
                winner.won_raffle = True
                winner.save()
                if winner.student:
                    winner.student.studentstatistics.raffles_won += 1
                    winner.student.studentstatistics.save()
                data['name'] = winner.name
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Request is missing the event id.")
    else:
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@require_http_methods(["GET", "POST"])
def event_checkin(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'GET':
        return HttpResponse(simplejson.dumps(get_attendees(event)), mimetype="application/json")
    else:
        email = request.POST.get('email', None).strip()
        if not email or not email_re.match(email):
            data = {
                'valid': False,
                'error': 'Enter a valid email!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        name = request.POST.get('name', None)
        student = None
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if hasattr(user, 'student'):
                student = user.student
        if not name and not student:
            data = {
                'valid': False,
                'error': "This email isn't registered with Umeqo. Enter your name!"
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if Attendee.objects.filter(event=event, email=email).exists():
            data = {
                'valid': False,
                'error': 'Duplicate checkin!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if not name:
            name = "%s %s" % (user.student.first_name, user.student.last_name)
        attendee = Attendee(email=email, name=name, student=student, event=event)
        try:
            attendee.save()
        except IntegrityError:
            data = {
                'valid': False,
                'error': 'Duplicate checkin!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if not student or student and not student.profile_created:
            if not student:
                template = 'checkin_follow_up.html'
            if student and not student.profile_created:
                template = 'checkin_follow_up_profile.html'
            subject = "[Umeqo] Event Check-In Follow-up"
            recipients = [email]
            body_context = {'name':name, 'current_site':Site.objects.get(id=s.SITE_ID), 'event':event, 'campus_org_event': is_campus_org(event.owner)}
            html_body = render_to_string(template, body_context)
            send_html_mail(subject, html_body, recipients)
        output = {
            'valid': True,
            'email': email
        }
        if student:
            output['name'] = student.first_name + ' ' + student.last_name
        else:
            output['name'] = name
        return HttpResponse(simplejson.dumps(output), mimetype="application/json")

@login_required
@agreed_to_terms
@user_passes_test(is_student)
@require_GET
def event_rsvp_message(request, extra_context=None):
    if request.GET.has_key("event_id"):
        try:
            e = Event.objects.get(id=request.GET['event_id'])
            if e.rsvp_message:
                context = {'event':e}
                if is_campus_org(e.owner):
                    context['is_campus_org_event'] = True
                return render_to_response("event_rsvp_message_dialog.html", context, context_instance=RequestContext(request))
            else:
                return HttpResponse()
        except Event.DoesNotExist:
            return HttpResponseBadRequest("Event with id %s does not exist." % (request.GET["event_id"]));
    return HttpResponseBadRequest("Event id is missing");

@login_required
@agreed_to_terms
@user_passes_test(is_student)
@render_to('events_list_ajax.html')
def event_search(request, extra_context=None):
    events = event_search_helper(request)
    context = {'events': events}
    context.update(extra_context or {})
    return context

@login_required
@agreed_to_terms
@user_passes_test(is_recruiter)
@has_annual_subscription
def events_by_employer(request):
    upcoming_events = Event.objects.filter(Q(owner=request.user) | Q(attending_employers__in=[request.user.recruiter.employer])).filter(Q(end_datetime__gte=datetime.now()) | Q(type__name="Rolling Deadline")).order_by("end_datetime")
    student_id, student = request.GET.get('student_id', None), None
    if student_id and not Student.objects.filter(id=student_id).exists():
        return HttpResponseBadRequest()
    elif student_id:
        student = Student.objects.get(id=student_id)
    def eventMap(event):
        invited = False
        if student and Invitee.objects.filter(event=event, student=student).exists():
            invited = True
        return {
            'id': event.id,
            'name': event.name,
            'is_public': event.is_public,
            'invited': invited,
        }
    events = map(eventMap, upcoming_events)
    return HttpResponse(simplejson.dumps(events), mimetype="application/json")

@login_required
@agreed_to_terms
@user_passes_test(is_recruiter)
@has_annual_subscription
@require_POST
def event_invite(request):
    event_id = request.POST.get('event_id', None)
    student_ids = request.POST.get('student_ids', None)
    message = request.POST.get('message', None)
    if not (event_id and student_ids and message):
        data = { 'valid': False, 'message': 'Missing data!' }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        data = { 'valid': False, 'message': 'Invalid event!' }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    event = event.get()
    student_ids = student_ids.split('~')
    students = []
    for student_id in student_ids:
        student = Student.objects.filter(id=student_id)
        if not student.exists():
            data = { 'valid': False, 'message': 'Invalid students.' }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        students.append(student.get())
    for student in students:
        invitee = Invitee.objects.filter(event=event, student=student)
        if invitee.exists():
            invitee = invitee.get()
            invitee.datetime_created = datetime.now()
            invitee.save()
        else:
            Invitee.objects.create(event=event, student=student)
        employer = request.user.recruiter.employer
        if event.is_public:
            notice_type = 'public_invite'
        else:
            notice_type = 'private_invite'
        notification.send([student.user], notice_type, {
            'name': student.user.first_name,
            'recruiter': request.user,
            'employer': employer,
            'event': event,
            'invite_message': message,
            'time_added': datetime.now(),
            'message': '<strong>%s</strong> has invited you to their event: "%s"' % (employer.name, event.name),
        })
    data = { 'valid': True, 'message': 'Invite sent successfully.' }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")