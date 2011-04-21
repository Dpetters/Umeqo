"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from employer.forms import SearchForm, DefaultFilteringParamsForm, FilteringForm
from student.models import Student
from employer.models import Employer
from employer.view_helpers import check_for_new_student_matches, filter_students, search_students, order_results
from core.decorators import is_employer
from digg_paginator.digg_paginator import DiggPaginator
from events.forms import EventForm
from events.models import Event
from notification.models import Notice
from student import constants as student_constants


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_home(request, username, template_name="employer_home.html", extra_context = None):
    if username == str(request.user):
        
        if request.useremployer.automatic_filtering_setup_completed:
            check_for_new_student_matches(request.user.employer)
        
        context = {
                   'search_form': SearchForm(),
                   'notices': Notice.objects.notices_for(request.user),
                   'unseen_notice_num': Notice.objects.unseen_count_for(request.user)
                   }
        
        context.update(extra_context or {})
        return render_to_response(template_name, 
                                  context, 
                                  context_instance=RequestContext(request))
    else:
        return redirect(reverse('employer_home', kwargs={'username': request.user}))

                                                 
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
def employer_setup_default_filtering_parameters(request,
                                                template_name = "employer_default_filtering_params_form.html",
                                                form_class=DefaultFilteringParamsForm,
                                                extra_context = None):
    
    if request.method == 'POST':
        form = form_class(data=request.POST,
                          instance = request.user.employer)
        if form.is_valid():
            form.save()
            request.user.employer.automatic_filtering_setup_completed = True
            request.user.employer.save()
            data = {"valid":True }
            return HttpResponse(simplejson.dumps(data))
        invalid_data = {"valid":True, 
                        "error": form.errors}
        return HttpResponse(simplejson.dumps(invalid_data))
    else:
        form = form_class(instance=request.user.employer)
    
    context = {
        'form':form
    }
    context.update(extra_context or {}) 
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_event(request,
                   template_name="employer_event.html",
                   extra_context=None):
    
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_event_summary(request, 
                           template_name="employer_event_summary.html",
                           extra_context=None):
    
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


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
                    template_name="employer/employer_events.html",
                    extra_context=None):
    
    context = {}
    context['upcoming_events'] = request.user.employer.events.filter(datetime__gt=datetime.datetime.now())
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_new_event(request, template_name = 'employer_new_event.html'):
    employer = Employer.objects.get(user__exact = request.user)
    if request.method == 'POST':
        form = EventForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            event_obj = form.save(commit=False)
            event_obj.employer = employer
            event_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            employer.events_posted +=1
            employer.save()
            return HttpResponseRedirect('/employer/events/' + str(event_obj.id))
        # WHAT HAPPENS IF THE FORM IS INVALID?
    return render_to_response(template_name, {'form':EventForm({'email':employer.user.email, 'datetime':datetime.datetime.now()})}, context_instance = RequestContext(request) )


def delete_event(request, template = 'employer_delete_event.html'): #@UnusedVariable
    if request.is_ajax():
        if request.method == 'POST':
            try:
                Event.objects.get(id=request.POST["event_id"]).delete()
                return HttpResponse(simplejson.dumps(request.POST["event_id"]), mimetype="application/json")
            except Event.DoesNotExist:
                return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return HttpResponseRedirect('/')
        
        
@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_filtering(request,
                       result_template_name='employer_results.html',
                       filtering_page_template_name='employer_filtering.html',
                       extra_context=None):
    context = {}
    
    if request.is_ajax():
        
        gpa=None
        if request.POST['gpa'] != "0":
            gpa = request.POST['gpa']
        
        act=None
        if request.POST['act'] != "0":
            act = request.POST['act']
        
        sat_t=None
        if request.POST['sat_t'] != "600":
            sat_t = request.POST['sat_t']
        
        sat_m=None
        if request.POST['sat_m'] != "200":
            sat_m = request.POST['sat_m']
        
        sat_v=None
        if request.POST['sat_v'] != "200":
            sat_v = request.POST['sat_v']
        
        sat_w=None
        if request.POST['sat_w'] != "200":
            sat_w = request.POST['sat_w']

        filtering_results = filter_students(gpa, act, sat_t, sat_m, sat_v, sat_w)
        
        search_results = []
        if request.POST['query'] != None:
            search_results = search_students(request.POST['query'])
        
        ordered_results = order_results(filtering_results, search_results, request.POST['ordering'])
        
        for student in ordered_results:
            student.shown_in_results_count += 1
            student.save()
        
        paginator = DiggPaginator(ordered_results, int(request.POST['results_per_page']), body=5, padding=1, margin=2) 

        context['page'] = paginator.page(request.POST['page'])
        
        context.update(extra_context or {})        
        return render_to_response(result_template_name, context, context_instance=RequestContext(request))

    else:
        if request.method == "POST" and request.POST.has_key('query'):
            form = SearchForm(data=request.POST)
            if form.is_valid():
                form.clean()
                context['query'] = form.cleaned_data['query']
        context['filtering_form'] = FilteringForm(initial={'ordering': request.user.employer.default_student_ordering, 'results_per_page' : request.user.employer.results_per_page})
        context['search_form'] = SearchForm()
        
    context.update(extra_context or {})
    return render_to_response(filtering_page_template_name, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_invitations(request, template_name='employer_invitations.html', extra_context=None):
    context = {}
    context.update(extra_context or {})  
    return render_to_response(template_name, context, context_instance=RequestContext(request))