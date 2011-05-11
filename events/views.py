"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from core.decorators import is_student
from events.models import Event
from django.utils import simplejson
from datetime import datetime

@login_required
def events_list(request, template_name='events_list.html', extra_context=None):
    events = Event.objects.all().filter(end_datetime__gte=datetime.now()).order_by("start_datetime")
    context = {
        'events': events
    }
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))


@login_required
def event_page(request, id, slug, template_name='event_page.html', extra_context=None):
    event = Event.objects.get(pk=id)
    #check slug matches event
    if event.slug!=slug:
        return HttpResponseNotFound()
    page_url = 'http://'+settings.DOMAIN+reverse('event_page',kwargs={'id':event.id,'slug':event.slug})
    context = {
        'event': event,
        'page_url': page_url,
        'show_rsvp': False,
        'attending': False
    }
    if hasattr(request.user,"student"):
        rsvp_events = request.user.student.event_set.all()
        if event in rsvp_events:
            context['attending'] = True
        else:
            context['show_rsvp'] = True
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def event_rsvp(request, id, template_name=None, extra_context=None):
    event = Event.objects.get(pk=id)
    event.rsvps.add(request.user.student)
    event.save()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}))
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def event_unrsvp(request, id, template_name=None, extra_context=None):
    event = Event.objects.get(pk=id)
    event.rsvps.remove(request.user.student)
    event.save()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}))
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))
