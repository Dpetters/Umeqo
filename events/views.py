from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.http import require_http_methods
from notification import models as notification

from core.decorators import is_recruiter, is_student, render_to
from events.models import Attendee, Event, RSVP, Invitee
from events.views_helper import event_search_helper
from student.models import Student

@login_required
@user_passes_test(is_student)
@render_to('events_list.html')
def events_list(request, extra_context=None):
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

def event_page(request, id, slug, extra_context=None):
    event = Event.objects.get(pk=id)
    if not hasattr(request.user,"recruiter"):
        event.view_count += 1
        event.save()
    is_past = event.end_datetime < datetime.now()    
    #check slug matches event
    if event.slug!=slug:
        return HttpResponseNotFound()
    current_site = Site.objects.get(id=settings.SITE_ID)
    page_url = 'http://' + current_site.domain + event.get_absolute_url()
    #google_description is the description + stuff to link back to umeqo
    google_description = event.description + '\n\nRSVP and more at %s' % page_url
    rsvps = map(buildRSVP, event.rsvp_set.all().order_by('student__first_name'))
    checkins = map(buildAttendee, event.attendee_set.all().order_by('name'))
    checkins.sort(key=lambda n: 0 if n['account'] else 1)
    emails_dict = {}
    all_responses = []
    for res in checkins + rsvps:
        if res['email'] not in emails_dict:
            emails_dict[res['email']] = 1
            all_responses.append(res)
    all_responses.sort(key=lambda n: n['datetime_created'])
    all_responses.sort(key=lambda n: 0 if n['account'] else 1)
    context = {
        'event': event,
        'rsvps': rsvps,
        'checkins': checkins,
        'all_responses': all_responses,
        'page_url': page_url,
        'DOMAIN': current_site.domain,
        'attending': False,
        'can_rsvp': False,
        'show_admin': False,
        'is_past': is_past,
        'recruiters': event.recruiters.all(),
        'google_description': google_description
    }
    if len(event.audience.all())>0:
        context['audience'] = event.audience.all()
    if hasattr(request.user,"student"):
        if RSVP.objects.filter(event=event, student=request.user.student).exists():
            context['attending'] = True
        context['can_rsvp'] = True
    elif hasattr(request.user,"recruiter"):
        context['show_admin'] = True
    
    context.update(extra_context or {})
    return render_to_response('event_page.html',context,context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def event_rsvp(request, id):
    event = Event.objects.get(pk=id)
    # if method is GET then get a list of RSVPed students
    if request.method == 'GET' and hasattr(request.user, 'recruiter'):
        data = map(lambda n: {'id': n.student.id, 'email': n.student.user.email}, event.rsvp_set.all())
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    # if POST then record student's RSVP
    elif request.method == 'POST' and hasattr(request.user, 'student'):
        rsvp = RSVP(student=request.user.student, event=event)
        rsvp.save()
        if request.is_ajax():
            return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
        else:
            return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))
    else:
        return HttpResponseForbidden()

@login_required
@user_passes_test(is_student)
def event_unrsvp(request, id):
    event = Event.objects.get(pk=id)
    rsvp = RSVP.objects.filter(student=request.user.student, event=event)
    rsvp.delete()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))

@login_required
@user_passes_test(is_recruiter)
@require_http_methods(["GET", "POST"])
def event_checkin(request, id):
    event = Event.objects.get(pk=id)
    if request.method == 'GET':
        attendees = map(buildAttendee, event.attendee_set.all().order_by('-datetime_created'))
        return HttpResponse(simplejson.dumps(attendees), mimetype="application/json")
    else:
        email = request.POST.get('email', None)
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
@render_to('events_list_ajax.html')
def event_search(request, extra_context=None):
    events = event_search_helper(request)
    context = {'events': events}
    context.update(extra_context or {})
    return context

@login_required
@user_passes_test(is_recruiter)
def events_by_employer(request):
    events = Event.objects.filter(recruiters=request.user.recruiter).filter(end_datetime__gte=datetime.now())
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
            'invited': invited
        }
    events = map(eventMap, events)
    return HttpResponse(simplejson.dumps(events), mimetype="application/json")

@login_required
@user_passes_test(is_recruiter)
@require_http_methods(["POST"])
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
        notification.send([student.user], 'public_invite', {
            'name': student.user.first_name,
            'recruiter': request.user.first_name + ' ' + request.user.last_name,
            'employer': employer.name,
            'event': event.name,
            'invite_message': message,
            'permalink': event.get_absolute_url(),
            'message': '<strong>%s</strong> has invited you to their event: "%s"' % (employer.name, event.name),
        })
        data = {
            'valid': True,
            'message': 'Invite sent successfully.'
        }
    else:
        data = {
            'valid': False,
            'message': 'Student has already been invited.'
        }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    
