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

def event_page(request, id, slug, template_name='event_page.html', extra_context=None):
    event = Event.objects.get(pk=id)
    if not hasattr(request.user,"recruiter"):
        event.view_count += 1
        event.save()
    is_past = event.end_datetime < datetime.now()    
    #check slug matches event
    if event.slug!=slug:
        return HttpResponseNotFound()
    page_url = 'http://'+settings.DOMAIN+reverse('event_page',kwargs={'id':event.id,'slug':event.slug})
    #google_description is the description + stuff to link back to umeqo
    google_description = event.description + '\n\nRSVP and more at %s' % page_url
    context = {
        'event': event,
        'rsvps': event.rsvps.all(),
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
        rsvp_events = request.user.student.event_set.all()
        if event in rsvp_events:
            context['attending'] = True
        context['can_rsvp'] = True
    elif hasattr(request.user,"recruiter"):
        context['show_admin'] = True
    
    context['company_logo'] = "http://"+settings.DOMAIN+settings.STATIC_URL+'images/company_logo_filler.png'
    
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def event_rsvp(request, id):
    event = Event.objects.get(pk=id)
    event.rsvps.add(request.user.student)
    event.save()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def event_unrsvp(request, id):
    event = Event.objects.get(pk=id)
    event.rsvps.remove(request.user.student)
    event.save()
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
    else:
        return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))

@login_required
def event_search(request, template_name='events_list_ajax.html', extra_context=None):
    search_results = search_helper(request.GET.get('q',''))
    events = map(lambda n: n.object, search_results)
    context = {
        'events': events
    }
    context.update(extra_context or {})
    return render_to_response(template_name,context,context_instance=RequestContext(request))
