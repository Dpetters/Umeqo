from __future__ import division
from __future__ import absolute_import

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.shortcuts import redirect, render_to_response
from django.template.loader import render_to_string

from core.email import send_html_mail
from core import messages as m
from core.decorators import is_recruiter, is_student, is_campus_org_or_recruiter, is_campus_org, render_to, has_annual_subscription
from core.models import Edit
from events.forms import EventForm, CampusOrgEventForm
from events.models import notify_about_event, Attendee, Event, EventType, Invitee, RSVP, DroppedResume
from events.views_helper import event_search_helper, buildAttendee, buildRSVP, get_event_schedule
from notification import models as notification
from student.models import Student

@login_required
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
    event = Event.objects.get(pk=id)
    return redirect("%s/%s" % (event.get_absolute_url(), event.slug))

@render_to('event_page.html')
def event_page(request, id, slug, extra_context=None):
    if is_student(request.user) and not request.user.student.profile_created:
        return redirect('student_profile')

    event = Event.objects.get(pk=id)

    #check slug matches event
    if event.slug!=slug:
        return HttpResponseNotFound("The slug you provided does not match that of the event found using the provided id.")

    current_site = Site.objects.get(id=settings.SITE_ID)

    page_url = 'http://' + current_site.domain + event.get_absolute_url()
    #google_description is the description + stuff to link back to umeqo
    google_description = event.description + '\n\nRSVP and more at %s' % page_url

    invitees = map(buildRSVP, event.invitee_set.all().order_by('student__first_name'))
    rsvps = map(buildRSVP, event.rsvp_set.filter(attending=True).order_by('student__first_name'))
    no_rsvps = map(buildRSVP, event.rsvp_set.filter(attending=False).order_by('student__first_name'))
    checkins = map(buildAttendee, event.attendee_set.all().order_by('name'))
    checkins.sort(key=lambda n: 0 if n['account'] else 1)

    emails_dict = {}
    all_responses = []
    for res in checkins + rsvps + no_rsvps:
        if res['email'] not in emails_dict:
            emails_dict[res['email']] = 1
            all_responses.append(res)
    all_responses.sort(key=lambda n: n['datetime_created'])
    all_responses.sort(key=lambda n: 0 if n['account'] else 1)
    
    context = {
        'event': event,
        'invitees': invitees,
        'rsvps': rsvps,
        'no_rsvps': no_rsvps,
        'checkins': checkins,
        'all_responses': all_responses,
        'page_url': page_url,
        'DOMAIN': current_site.domain,
        'current_site':"http://" + current_site.domain,
        'is_deadline': (event.type == EventType.objects.get(name='Hard Deadline') or event.type == EventType.objects.get(name='Rolling Deadline')),
        'google_description': google_description
    }
    if event.end_datetime:
        context['is_past'] = event.end_datetime < datetime.now()
    else:
        context['is_rolling_deadline'] = True
        
    if len(event.audience.all()) > 0:
        context['audience'] = event.audience.all()
    
    if is_campus_org(event.owner):
        context['campus_org_event'] = True
        context['attending_employers'] = event.attending_employers
        if is_campus_org(request.user):
            context['resume_drops'] = len(event.droppedresume_set.all())
            context['can_edit'] = (event.owner == request.user)
    elif is_recruiter(event.owner):
        if is_recruiter(request.user):
            context['can_edit'] = request.user.recruiter in event.owner.recruiter.employer.recruiter_set.all()
            
    if not is_campus_org(request.user) and not is_recruiter(request.user):
        event.view_count += 1
        event.save()
            
    if is_student(request.user):
        
        rsvp = RSVP.objects.filter(event=event, student=request.user.student)
        
        if rsvp.exists():
            context['attending'] = rsvp.get().attending
            context['responded'] = True
        
        dropped_resume = DroppedResume.objects.filter(event=event, student=request.user.student)
        if dropped_resume.exists():
            context['dropped_resume'] = True
        
        context['can_rsvp'] = True
    context.update(extra_context or {})
    return context

@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@render_to()
def event_new(request, form_class=None, extra_context=None):
    context = {'TEMPLATE':"event_form.html"}
    if is_recruiter(request.user):
        form_class = EventForm
    elif is_campus_org(request.user):
        form_class = CampusOrgEventForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            form.save_m2m()
            if is_recruiter(request.user):
                event.attending_employers.add(request.user.recruiter.employer);
            notify_about_event(event, "new_event", event.attending_employers.all())
            return HttpResponseRedirect(reverse('event_page', kwargs={'id':event.id, 'slug':event.slug}))
    else:
        form = form_class(initial={
            'start_datetime': datetime.now(),
            'end_datetime': datetime.now() + timedelta(hours=1),
        })
    context['hours'] = map(lambda x,y: str(x) + y, [12] + range(1,13) + range(1,12), ['am']*12 + ['pm']*12)
    context['form'] = form
    context.update(extra_context or {})
    return context

@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@render_to("event_form.html")
def event_edit(request, id=None, extra_context=None):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event with id %s not found." % id)        
    context = {}
    context['event'] = event
    if is_recruiter(event.owner):
        form_class = EventForm
        if not is_recruiter(request.user) or request.user.recruiter.employer != event.owner.recruiter.employer:
            return HttpResponseForbidden('You are not allowed to edit this event.')                
    elif is_campus_org(event.owner):
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
    if event.type.name == "Hard Deadline":
        context['event_scheduler_date'] = event.end_datetime.strftime('%m/%d/%Y')
    elif event.type.name == "Rolling Deadline":
        context['event_scheduler_date'] = datetime.now().strftime('%m/%d/%Y')
    else:
        context['event_scheduler_date'] =  event.start_datetime.strftime('%m/%d/%Y')
    context.update(extra_context or {})
    return context

@login_required
@has_annual_subscription
@user_passes_test(is_campus_org_or_recruiter)
def event_delete(request, id, extra_context = None):
    if request.is_ajax():
        try:
            event = Event.objects.get(pk=id)
            if is_recruiter(event.owner):
                if not is_recruiter(request.user) or request.user.recruiter.employer != event.owner.recruiter.employer:
                    return HttpResponseForbidden('You are not allowed to delete this event.')                
            elif is_campus_org(event.owner):
                if not is_campus_org(request.user) or request.user.campusorg != event.owner.campusorg:
                    return HttpResponseForbidden('You are not allowed to delete this event.') 
            event.is_active = False

            event.save()
            return HttpResponse()
        except Event.DoesNotExist:
            return HttpResponseNotFound("Event with id %s not found." % id)
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
def event_schedule(request):
    if request.is_ajax():
        schedule = get_event_schedule(request.GET.get('event_date', datetime.now().strftime('%m/%d/%Y')))
        return HttpResponse(simplejson.dumps(schedule), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
@require_http_methods(["GET", "POST"])
@has_annual_subscription
def event_rsvp(request, event_id):
    event = Event.objects.get(pk=event_id)
    # if method is GET then get a list of RSVPed students
    if request.method == 'GET' and is_recruiter(request.user) or is_campus_org(request.user):
        data = map(lambda n: {'id': n.student.id, 'email': n.student.user.email}, event.rsvp_set.all())
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    # if POST then record student's RSVP
    elif request.method == 'POST' and hasattr(request.user, 'student'):
        isAttending = request.POST.get('isAttending', 'true')
        isAttending = True if isAttending=='true' else False
        rsvp = RSVP.objects.filter(student=request.user.student, event=event)
        if rsvp.exists():
            rsvp = rsvp.get()
            rsvp.attending = isAttending
            if isAttending:
                # Also "drop" the resume.
                DroppedResume.objects.get_or_create(event=event, student=request.user.student)
            else:
                # Also "undrop" the resume.
                DroppedResume.objects.filter(event=event, student=request.user.student).delete()
            rsvp.save()
        else:
            RSVP.objects.create(student=request.user.student, event=event, attending=isAttending)
        if request.is_ajax():
            return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
        else:
            return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))
    else:
        return HttpResponseForbidden("You must be a recruiter or campus org to access this view.")

@login_required
@user_passes_test(is_student)
def event_unrsvp(request, event_id):
    event = Event.objects.get(pk=event_id)
    rsvp = RSVP.objects.filter(student=request.user.student, event=event)
    rsvp.delete()

    # Also "undrop" the resume.
    DroppedResume.objects.filter(event=event, student=request.user.student).delete()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))

@login_required
@user_passes_test(is_student)
@require_POST
def event_drop(request, event_id):
    data = {}
    if not event_id:
        data.update({
            'valid': False,
            'message': 'Invalid event id.'
        })
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        data.update({
            'valid': False,
            'message': 'Invalid event id.'
        })
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    event = event.get()
    student = request.user.student
    DroppedResume.objects.get_or_create(event=event, student=student)
    data.update({
        'valid': True,
        'message': 'Resume dropped.'
    })
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@login_required
@user_passes_test(is_student)
@require_POST
def event_undrop(request, event_id):
    event = Event.objects.filter(id=event_id)
    DroppedResume.objects.filter(event=event, student=request.user.student).delete()
    return HttpResponse(simplejson.dumps({'valid': True}), mimetype="application/json")

@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@require_http_methods(["GET", "POST"])
def event_checkin(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'GET':
        attendees = map(buildAttendee, event.attendee_set.all().order_by('-datetime_created'))
        return HttpResponse(simplejson.dumps(attendees), mimetype="application/json")
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
        if not name:
            name = "%s %s" % (user.student.first_name, user.student.last_name)
        if not student:
            subject = "[umeqo.com] %s Check-In Follow-up" % str(event)
            recipients = [email]
            body_context = {'name':name, 'current_site':Site.objects.get(id=settings.SITE_ID), 'event':event, 'campus_org_event': is_campus_org(event.owner)}
            html_body = render_to_string('checkin_follow_up.html', body_context)
            send_html_mail(subject, html_body, recipients)
        if student and not student.profile_created:
            subject = "[umeqo.com] %s Check-In Follow-up" % str(event)
            recipients = [email]
            body_context = {'name':name, 'current_site':Site.objects.get(id=settings.SITE_ID), 'event':event}
            html_body = render_to_string('checkin_follow_up_profile.html', body_context)
            send_html_mail(subject, html_body, recipients)
        attendee = Attendee(email=email, name=name, student=student, event=event)
        try:
            attendee.save()
        except IntegrityError:
            data = {
                'valid': False,
                'error': 'Duplicate checkin!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
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
@user_passes_test(is_student)
@render_to('events_list_ajax.html')
def event_search(request, extra_context=None):
    events = event_search_helper(request)
    context = {'events': events}
    context.update(extra_context or {})
    return context

@login_required
@user_passes_test(is_recruiter)
@has_annual_subscription
def events_by_employer(request):
    upcoming_events = request.user.event_set.active().filter(Q(end_datetime__gte=datetime.now()) | Q(type__name="Rolling Deadline"))
    student_id = request.GET.get('student_id', None)
    if not student_id or not Student.objects.filter(id=student_id).exists():
        return HttpResponseBadRequest()
    student = Student.objects.get(id=student_id)
    def eventMap(event):
        invited = False
        if Invitee.objects.filter(event=event, student=student).exists():
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
@user_passes_test(is_recruiter)
@has_annual_subscription
@require_POST
def event_invite(request):
    event_id = request.POST.get('event_id', None)
    student_id = request.POST.get('student_id', None)
    message = request.POST.get('message', None)
    if not (event_id and student_id and message):
        return HttpResponseBadRequest()
    event = Event.objects.filter(id=event_id)
    student = Student.objects.filter(id=student_id)
    if not (student.exists() and event.exists()):
        return HttpResponseBadRequest()
    event = event.get()
    student = student.get()
    if not Invitee.objects.filter(event=event, student=student).exists():
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
    else:
        data = {'valid': False, 'message': m.already_invited }

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")