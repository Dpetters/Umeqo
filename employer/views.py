"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import datetime

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils import simplejson

from employer.forms import SearchForm, FilteringForm, StudentFilteringForm
from student.models import Student
from employer.models import Employer
from employer.view_helpers import filter_students, search_students, combine_and_order_results
from core.decorators import is_employer
from core.digg_paginator import DiggPaginator
from events.forms import EventForm
from events.models import Event
from student import constants as student_constants


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_company_profile(request, username, 
                             template_name="employer_company_profile.html", 
                             extra_context = None):
    if username == str(request.user):
        context = {}
        context.update(extra_context or {})
        return render_to_response(template_name, 
                                  context, 
                                  context_instance=RequestContext(request))
    else:
        return redirect(reverse('employer_company_profile', kwargs={'username': request.user}))

    
def employer_registration(request, 
                           template_name="employer_registration.html", 
                           extra_context = None):
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_add_to_resume_book(request, student_id):
    if request.ajax():
        employer = Employer.objects.get(user__exact = request.user)
        employer.studentlist_set.get(name=student_constants.IN_CURRENT_RESUME_BOOK_STUDENT_GROUP_NAME).add(Student.objects.get(id=student_id))
        return HttpResponse(simplejson.dumps({"valid":True}))
    redirect('home')


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_account_settings(request, 
                              template_name="employer_account_settings.html", 
                              extra_context=None):
    
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_events(request,
                    template_name="employer_events.html",
                    extra_context=None):
    
    context = {
        'upcoming_events': request.user.employer.event_set.filter(end_datetime__gte=datetime.datetime.now()).order_by("start_datetime")
    }
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_new_event(request, template_name='employer_new_event.html', extra_context=None):
    if request.method == 'POST':
        form = EventForm(data=request.POST)
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.employer = request.user.employer
            event_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(reverse('event_page',kwargs={'id':event_obj.id,'slug':event_obj.slug}))
    else:
        form = EventForm({'start_datetime':datetime.datetime.now()})
        
    context = {
        'form': form
    }
    
    context.update(extra_context or {})
    return render_to_response(template_name, 
                              context,
                              context_instance = RequestContext(request))

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_edit_event(request, id=None, template_name='employer_new_event.html', extra_context=None):
    event = Event.objects.get(pk=id)
    if event.employer!=request.user.employer:
        return HttpResponseForbidden('not your event!')
    if request.method=='POST':
        form = EventForm(request.POST,instance=event)
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.employer = request.user.employer
            event_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(reverse('event_page',kwargs={'id':event_obj.id,'slug':event_obj.slug}))
    else:
        form = EventForm(instance=event)
    context = {
        'form': form,
        'edit': True
    }

    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance = RequestContext(request) )

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_delete_event(request,
                          id,
                          extra_context = None):
    try:
        event = Event.objects.get(pk=id)
        if event.employer!=request.user.employer:
            return HttpResponseForbidden('not your event!')
        event.is_active = False
        event.save()
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(id), mimetype="application/json")
        else:
            return HttpResponseRedirect(reverse('home'))
    except Event.DoesNotExist:
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_setup_default_filtering(request,
                                    template_name = "employer_setup_default_filtering.html",
                                    form_class=FilteringForm,
                                    extra_context = None):
    
    if request.method == 'POST':
        form = form_class(data=request.POST,
                          instance = request.user.employer)
        if form.is_valid():
            form.save()
            request.user.employer.automatic_filtering_setup_completed = True
            request.user.employer.save()
    else:
        form = form_class(instance=request.user.employer)
    
    context = {
        'form':form
    }
    context.update(extra_context or {}) 
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


def get_cached_paginator(request):
    cached_paginator = cache.get('paginator')
    if cached_paginator:
        return cached_paginator
    else:
        current_paginator = DiggPaginator(get_cached_ordered_results(request), int(request.POST['results_per_page']), body=5, padding=1, margin=2)
        cache.set('paginator', current_paginator)
        return current_paginator
    
def get_cached_ordered_results(request):
    cached_ordered_results = cache.get('ordered_results')
    if cached_ordered_results:
        return cached_ordered_results
    else:
        current_ordered_results = combine_and_order_results(get_cached_filtering_results(request), get_cached_search_results(request), request.POST['ordering'], request.POST['query'])
        cache.set('ordered_results', current_ordered_results)
        return current_ordered_results
    
def get_cached_filtering_results(request):
    cached_filtering_results = cache.get('filtering_results')
    if cached_filtering_results:
        return cached_filtering_results
    else:
        gpa = None
        if request.POST['gpa'] != "0":
            gpa = request.POST['gpa']
        
        act = None
        if request.POST['act'] != "0":
            act = request.POST['act']
        
        sat_t = None
        if request.POST['sat_t'] != "600":
            sat_t = request.POST['sat_t']

        sat_m = None
        if request.POST['sat_m'] != "200":
            sat_m = request.POST['sat_m']
            
        sat_v = None
        if request.POST['sat_v'] != "200":
            sat_v = request.POST['sat_v']

        sat_w = None
        if request.POST['sat_w'] != "200":
            sat_w = request.POST['sat_w']

        courses = None
        if request.POST['courses']:
            courses = request.POST['courses'].split('~');
        
        school_years = None
        if request.POST['school_years']:
            school_years = request.POST['school_years'].split('~');
            
        graduation_years = None
        if request.POST['graduation_years']:
            graduation_years = request.POST['graduation_years'].split('~');
        
        employment_types = None
        if request.POST['employment_types']:
            employment_types = request.POST['employment_types'].split('~');

        previous_employers = None
        if request.POST['previous_employers']:
            previous_employers = request.POST['previous_employers'].split('~');
        
        industries_of_interest = None
        if request.POST['industries_of_interest']:
            industries_of_interest = request.POST['industries_of_interest'].split('~');
        
        citizen = None
        if request.POST['citizen'] != "False":
            citizen = request.POST['citizen']
            
        older_than_18 = None
        if request.POST['older_than_18'] != "False":
            older_than_18 = request.POST['older_than_18']
                    
        current_filtering_results = filter_students(student_list=request.POST['student_list'],
                                                    gpa=gpa,
                                                    courses = courses,
                                                    school_years = school_years,
                                                    graduation_years = graduation_years,
                                                    act=act,
                                                    sat_t=sat_t,
                                                    sat_m=sat_m,
                                                    sat_v=sat_v,
                                                    sat_w=sat_w,
                                                    employment_types=employment_types,
                                                    previous_employers=previous_employers,
                                                    industries_of_interest=industries_of_interest,
                                                    citizen = citizen,
                                                    older_than_18 = older_than_18)
        
        cache.set('filtering_results', current_filtering_results)
    return current_filtering_results

def get_cached_search_results(request):
    current_search_results = []
    if request.POST['query'] != "null":
        current_search_results = search_students(request.POST['query'])
    cache.set('search_results', current_search_results)
    return current_search_results

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_student_filtering(request,
                               result_template_name='employer_student_filtering_results.html',
                               filtering_page_template_name='employer_student_filtering.html',
                               extra_context=None):
    
    context = {}
    if request.is_ajax():
        cached_page = cache.get('page')
        if cached_page and cached_page != int(request.POST['page']):
            cache.set('page', int(request.POST['page']))
        else:
            if request.POST['page'] and not cached_page:
                cache.set('page', int(request.POST['page']))
            cached_results_per_page = cache.get('results_per_page')
            if cached_results_per_page and cached_results_per_page != int(request.POST['results_per_page']):
                cache.set('results_per_page', int(request.POST['results_per_page']))
                cache.delete('paginator')
            else:
                if int(request.POST['results_per_page']) and not cached_results_per_page:
                    cache.set('results_per_page', int(request.POST['results_per_page']))
                cached_ordering = cache.get('ordering')
                if cached_ordering and cached_ordering != request.POST['ordering']:
                    cache.set('ordering', request.POST['ordering'])
                    cache.delete('paginator')
                    cache.delete('ordered_results')
                else:
                    if request.POST['ordering'] and not cached_ordering:
                        cache.set('ordering', request.POST['ordering'])
                    cached_query = cache.get('query')
                    if cached_query and cached_query != request.POST['query']:
                        cache.set('query', request.POST['query'])
                        cache.delete('paginator')
                        cache.delete('ordered_results')
                        cache.delete('search_results')
                    else:
                        if request.POST['query'] and not cached_query:
                            cache.set('query', request.POST['query'])
                        cache.delete('paginator')
                        cache.delete('ordered_results')
                        cache.delete('filtering_results')

        current_paginator = get_cached_paginator(request)      
        context['page'] = current_paginator.page(request.POST['page'])
        
        for student in context['page'].object_list:
            student.shown_in_results_count += 1
            student.save()
        
        context.update(extra_context or {}) 
        return render_to_response(result_template_name, context, context_instance=RequestContext(request))
    else:
        if request.method == "POST" and request.POST.has_key('query'):
                context['query'] = request.POST.get('query', '')

        context['student_filtering_form'] = StudentFilteringForm({'employer': request.user.employer},
                                                                 initial={'ordering': request.user.employer.default_student_ordering,                           
                                                                          'results_per_page' : request.user.employer.results_per_page})
        context['student_search_form'] = SearchForm()
        
    context.update(extra_context or {})
    return render_to_response(filtering_page_template_name, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_invitations(request, template_name='employer_invitations.html', extra_context=None):
    context = {}
    context.update(extra_context or {})  
    return render_to_response(template_name, context, context_instance=RequestContext(request))
