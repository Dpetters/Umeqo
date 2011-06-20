"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from core.decorators import is_recruiter, is_student
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.http import require_http_methods
from events.models import Attendee, Event, RSVP
from haystack.query import SearchQuerySet

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def events_list(request, template_name='events_list.html', extra_context=None):
    query = request.GET.get('q','')
    search_results = search_helper(query)
    #we use map to extract the object for each event
    events = map(lambda n: n.object,search_results)
    context = {
        'events': events,
        'query': query
    }
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))

def search_helper(query):
    search_results = SearchQuerySet().models(Event).filter(end_datetime__gte=datetime.now()).order_by("start_datetime")
    if query!="":
        for q in query.split(' '):
            if q.strip()!="":
                search_results = search_results.filter(content_auto=q)
    print search_results
    return search_results

def event_page_redirect(request, id):
    event = Event.objects.get(pk=id)
    return redirect(reverse('event_page', kwargs={'id':event.id,'slug':event.slug}))

def event_page(request, id, slug, template_name='event_page.html', extra_context=None):
    event = Event.objects.get(pk=id)
    if not hasattr(request.user,"recruiter"):
        event.view_count += 1
        event.save()
    is_past = event.end_datetime < datetime.now()    
    #check slug matches event
    if event.slug!=slug:
        return HttpResponseNotFound()
    page_url = 'http://'+settings.DOMAIN+reverse('event_page', kwargs={'id':event.id,'slug':event.slug})
    #google_description is the description + stuff to link back to umeqo
    google_description = event.description + '\n\nRSVP and more at %s' % page_url
    checkins = map(lambda n: n.student, event.attendee_set.all().order_by('-datetime_created'))
    rsvps = map(lambda n: n.student, event.rsvp_set.all())
    context = {
        'event': event,
        'checkins': checkins,
        'rsvps': rsvps,
        'page_url': page_url,
        'DOMAIN': settings.DOMAIN,
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
    
    context['company_logo'] = "http://"+settings.DOMAIN+settings.STATIC_URL+'images/company_logo_filler.png'
    
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
@require_http_methods(["GET", "POST"])
def event_rsvp(request, id):
    event = Event.objects.get(pk=id)
    # if method is GET then get a list of RSVPed students
    if request.method == 'GET' and hasattr(request.user, 'recruiter'):
        data = map(lambda n: {'id': n.id, 'email': n.user.email}, event.rsvps.all())
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
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def event_unrsvp(request, id):
    event = Event.objects.get(pk=id)
    rsvp = RSVP.objects.filter(student=request.user.student, event=event)
    rsvp.delete()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
@require_http_methods(["GET", "POST"])
def event_checkin(request, id):
    event = Event.objects.get(pk=id)
    if request.method == 'GET':
        def buildAttendee(obj):
            output = {'email': obj.email}
            if obj.student:
                output['name'] = obj.student.first_name + ' ' + obj.student.last_name
            else:
                output['name'] = obj.name
            return output
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

        attendee = Attendee(email=email, name=name, student=student, event=event)
        attendee.save()
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
def event_search(request, template_name='events_list_ajax.html', extra_context=None):
    search_results = search_helper(request.GET.get('q',''))
    events = map(lambda n: n.object, search_results)
    context = {
        'events': events
    }
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))
