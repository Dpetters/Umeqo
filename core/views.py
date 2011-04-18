"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import datetime
 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache

from events.models import Event

@never_cache
def home(request,
         template_name="home.html",
         extra_context=None):
    
    if request.user.is_authenticated():
        if hasattr(request.user, "student"):
            url = "/student/"
        elif hasattr(request.user, "employer"):
            url = "/employer/"
        return HttpResponseRedirect(url + str(request.user) + "/")
    
    context = {}
    
    context['action'] = request.REQUEST.get('action', '')
    
    event_kwargs = {}
    event_kwargs['datetime__gt'] = datetime.datetime.now()
    events = Event.objects.filter(**event_kwargs).order_by("-datetime_created")
    context['events'] = list(events)[:3]
    
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))