"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from events.models import Event
from django.core.urlresolvers import reverse

@login_required
def event_page(request,
               id,slug,
               template_name='event_page.html',
               extra_context=None):
    event = Event.objects.get(pk=id)
    #check slug matches event
    if event.slug!=slug:
        return HttpResponseNotFound()
    context = {
        'event': event,
        'page_url': 'http://'+settings.DOMAIN+reverse('event_page',kwargs={'id':event.id,'slug':event.slug})
    }
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
def event_rsvp(request,
               id,status,
               template_name=None,
               extra_context=None):
    event = Event.objects.get(pk=id)
    pass