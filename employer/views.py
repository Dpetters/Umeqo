"""
 Developers : Dmitrij Petters, Joshua Ma
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from datetime import datetime

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import simplejson

from employer.models import ResumeBook
from employer.forms import EmployerPreferences, SearchForm, FilteringForm, StudentFilteringForm, StudentCommentForm
from employer.view_helpers import get_cached_paginator
from employer import enums as employer_enums
from employer import snippets as employer_snippets

from core.decorators import is_recruiter
from events.forms import EventForm
from events.models import Event
from student.models import Student

def employer_registration(request, 
                           template_name="employer_registration.html", 
                           extra_context = None):
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
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

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_preferences(request, 
                         template_name="employer_preferences.html", 
                         form_class = EmployerPreferences,
                         extra_context=None):
    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES, instance=request.user.recruiter)
            if form.is_valid():
                data = {'valid':True}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                data = {'valid':False,
                        'form_errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            form = form_class(instance=request.user.recruiter)
    
        context = {
                   'form' : form
                   }
        context.update(extra_context or {})
        return render_to_response(template_name,
                                  context,
                                  context_instance=RequestContext(request))
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_account_settings(request, 
                              template_name="employer_account_settings.html", 
                              extra_context=None):
    
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_star_student_toggle(request,
                                 extra_context=None):
    
    if request.is_ajax():
        if request.POST.has_key('student_id'):
            student = Student.objects.get(id=request.POST['student_id'])
            if student in request.user.recruiter.starred_students.all():
                request.user.recruiter.starred_students.remove(student)
                data = {'valid':True,
                        'action':employer_enums.UNSTARRED}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")    
            else:
                request.user.recruiter.starred_students.add(student)
                data = {'valid':True,
                        'action':employer_enums.STARRED}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Student ID is missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_star_students_add(request,
                               extra_context=None):
    
    if request.is_ajax():
        print request.POST
        if request.POST.has_key('student_ids'):
            for id in request.POST['student_ids'].split('~'):
                student = Student.objects.get(id=id)  
                if student not in request.user.recruiter.starred_students.all():
                    request.user.recruiter.starred_students.add(student)
            data = {'valid':True}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Student IDs are missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_star_students_remove(request,
                                  extra_context=None):
    
    if request.is_ajax():
        if request.POST.has_key('student_ids'):
            for id in request.POST['student_ids'].split('~'):
                student = Student.objects.get(id=id)  
                if student in request.user.recruiter.starred_students.all():
                    request.user.recruiter.starred_students.remove(student)
            data = {'valid':True}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Student IDs are missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_book_student_toggle(request,
                                        extra_context=None):
    
    if request.is_ajax():
        if request.POST.has_key('student_id'):
            student = Student.objects.get(id=request.POST['student_id'])
            resume_books = ResumeBook.objects.filter(recruiter = request.user.recruiter)
            if not resume_books.exists():
                latest_resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
            else:
                latest_resume_book = resume_books.order_by('-date_created')[0]
            if student in latest_resume_book.students.all():
                latest_resume_book.students.remove(student)
                data = {'valid':True,
                        'action':employer_enums.REMOVED}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")    
            else:
                latest_resume_book.students.add(student)
                data = {'valid':True,
                        'action':employer_enums.ADDED}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Student ID is missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_book_students_add(request,
                                         extra_context=None):
    
    if request.is_ajax():
        if request.POST.has_key('student_ids'):
            resume_books = ResumeBook.objects.filter(recruiter = request.user.recruiter)
            if not resume_books.exists():
                latest_resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
            else:
                latest_resume_book = resume_books.order_by('-date_created')[0]
            for id in request.POST['student_ids'].split('~'):
                student = Student.objects.get(id=id)  
                if student not in latest_resume_book.students.all():
                    latest_resume_book.students.add(student)
            data = {'valid':True}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Student IDs are missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_book_students_remove(request,
                                              extra_context=None):
    
    if request.is_ajax():
        if request.POST.has_key('student_ids'):
            resume_books = ResumeBook.objects.filter(recruiter = request.user.recruiter)
            if not resume_books.exists():
                latest_resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
            else:
                latest_resume_book = resume_books.order_by('-date_created')[0]
            for id in request.POST['student_ids'].split('~'):
                student = Student.objects.get(id=id)  
                if student in latest_resume_book.students.all():
                    latest_resume_book.students.remove(student)
            data = {'valid':True}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Student IDs are missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_events(request,
                    template_name="employer_events.html",
                    extra_context=None):
    
    context = {
        'upcoming_events': request.user.recruiter.event_set.filter(end_datetime__gte=datetime.now()).order_by("start_datetime")
    }
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_new_event(request, template_name='employer_new_event.html', extra_context=None):
    if request.method == 'POST':
        form = EventForm(data=request.POST)
        if form.is_valid():
            event_obj = form.save()
            event_obj.recruiters.add(request.user.recruiter)
            event_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(reverse('event_page',kwargs={'id':event_obj.id,'slug':event_obj.slug}))
    else:
        form = EventForm()

    context = {
        'form': form
    }
    
    context.update(extra_context or {})
    return render_to_response(template_name, 
                              context,
                              context_instance = RequestContext(request))

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_edit_event(request, id=None, template_name='employer_new_event.html', extra_context=None):
    event = Event.objects.get(pk=id)
    if not request.user.recruiter in event.recruiters.all():
        return HttpResponseForbidden('not your event!')
    if request.method=='POST':
        form = EventForm(request.POST,instance=event)
        if form.is_valid():
            event_obj = form.save()
            event_obj.recruiters.clear()
            event_obj.recruiters.add(request.user.recruiter)
            event_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(reverse('event_page',kwargs={'id':event_obj.id,'slug':event_obj.slug}))
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'edit': True,
        'event': {
            'id': event.id,
            'slug': event.slug
        }
    }

    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance = RequestContext(request) )

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_delete_event(request,
                          id,
                          extra_context = None):
    try:
        event = Event.objects.get(pk=id)
        if request.user.recruiter not in event.recruiters.all():
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
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_setup_default_filtering(request,
                                    template_name = "employer_setup_default_filtering.html",
                                    form_class=FilteringForm,
                                    extra_context = None):
    
    if request.method == 'POST':
        form = form_class(data=request.POST,
                          instance = request.user.recruiter)
        if form.is_valid():
            form.save()
            request.user.recruiter.automatic_filtering_setup_completed = True
            request.user.recruiter.save()
    else:
        form = form_class(instance=request.user.recruiter)
    
    context = {
        'form':form
    }
    context.update(extra_context or {}) 
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))




@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_book_summary(request,
                                 template_name="employer_resume_book_summary.html",
                                 extra_context=None):
    if request.is_ajax():
        resume_books = ResumeBook.objects.filter(recruiter = request.user.recruiter)
        if not resume_books.exists():
            latest_resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
        else:
            latest_resume_book = resume_books.order_by('-date_created')[0]
            context = {}
            context['resume_book'] = latest_resume_book
            context.update(extra_context or {}) 
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_student_filtering(request,
                               result_template_name='employer_student_filtering_results.html',
                               filtering_page_template_name='employer_student_filtering.html',
                               extra_context=None):
    
    context = {}
    context['add_to_resume_book_img'] = employer_snippets.add_to_resumebook_img
    context['remove_from_resume_book_img'] = employer_snippets.remove_from_resumebook_img
    context['starred_img'] = employer_snippets.starred_img
    context['unstarred_img'] = employer_snippets.unstarred_img
    
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
        context['student_comment_form'] = StudentCommentForm()
        for student, is_in_resume_book, is_starred in context['page'].object_list:
            student.statistics.shown_in_results_count += 1
            student.save()
        
        context.update(extra_context or {}) 
        return render_to_response(result_template_name, context, context_instance=RequestContext(request))
    else:
        cache.delete('paginator')
        cache.delete('ordered_results')
        cache.delete('filtering_results')
        cache.delete('search_results')
        if request.method == "POST" and request.POST.has_key('query'):
                context['query'] = request.POST.get('query', '')
                
        context['student_filtering_form'] = StudentFilteringForm({'recruiter': request.user.recruiter},
                                                                 initial={'ordering': request.user.recruiter.preferences.default_student_ordering,                           
                                                                          'results_per_page' : request.user.recruiter.preferences.results_per_page})
        context['student_search_form'] = SearchForm()
        context['added'] = employer_enums.ADDED
        context['removed'] = employer_enums.REMOVED
        context['starred'] = employer_enums.STARRED
        context['unstarred'] = employer_enums.UNSTARRED
        
    context.update(extra_context or {})
    return render_to_response(filtering_page_template_name, context, context_instance=RequestContext(request))


@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_invitations(request, template_name='employer_invitations.html', extra_context=None):
    context = {}
    context.update(extra_context or {})  
    return render_to_response(template_name, context, context_instance=RequestContext(request))
