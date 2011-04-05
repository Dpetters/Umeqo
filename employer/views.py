"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache #@UnusedImport
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Q
from django.utils import simplejson

from employer.forms import SearchForm, DefaultFilteringParamsForm, FilteringForm
from student.models import Student
from employer.models import Employer
from core.decorators import is_employer
from digg_paginator.digg_paginator import DiggPaginator
from events.forms import EventForm
from events.models import Event
from notification import models as notification
from haystack.query import SearchQuerySet
from notification.models import Notice

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_home(request, username, template_name="employer_home.html"):
    if username == str(request.user):
        employer = Employer.objects.get(user = request.user)
        
        if employer.automatic_filtering_setup_completed:
            check_for_new_student_matches(employer)
        
        data = {}
        data['user'] = employer
        data['form'] = SearchForm()
        data['notices'] = Notice.objects.notices_for(request.user)
        data['unseen_notice_num'] = Notice.objects.unseen_count_for(request.user)
        
        return render_to_response(template_name, data, context_instance=RequestContext(request))
    else:
        try:
            Employer.objects.get(user__username=username)
            return HttpResponseRedirect("/employer/" + str(request.user))
        except Employer.DoesNotExist:
            return HttpResponseNotFound("404.html")

def check_for_new_student_matches(employer):
    all_student_matches = filter_students(gpa=employer.gpa,
                                          act=employer.act,
                                          sat_t = employer.sat_t,
                                          sat_v = employer.sat_v,
                                          sat_m = employer.sat_m,
                                          sat_w = employer.sat_w)
    new_student_matches = []
    for student in all_student_matches:
        if student not in employer.last_seen_students.all():
            new_student_matches.append(student)
            
    employer.new_students = new_student_matches
    employer.save()
    
    notification.send([employer.user], 'new_student_matches', {'students':new_student_matches})
                                                 
def employer_register(request, template_name="employer_registration.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_add_to_resume_book(request, student_id):
    employer = Employer.objects.get(user__exact = request.user)
    employer.cart.add(Student.objects.get(id=student_id))
    return HttpResponse(simplejson.dumps({"valid":True}))
    
def filter_students(gpa=None, act=None, sat_t=None, sat_m=None, sat_v=None, sat_w=None, courses=None):
    kwargs = {}    
    
    all_students = Student.objects.all()
    
    if gpa:
        kwargs['gpa__gte'] = gpa
    if act:
        kwargs['act__gte'] = act
    if sat_t:
        kwargs['sat_t__gte'] = sat_t
    if sat_m:
        kwargs['sat_m__gte'] = sat_m
    if sat_v:
        kwargs['sat_v__gte'] = sat_v
    if sat_w:
        kwargs['sat_w__gte'] = sat_w
        
    filtering_results = all_students.filter(**kwargs)
    
    if courses:
        filtering_results = filtering_results.filter(Q(first_major__name__in=courses) | Q(second_major__name__in=courses))
    
    return filtering_results
    
    
@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_setup_default_filtering_parameters(request,
                                                template_name = "employer_default_filtering_params_form.html",
                                                form_class=DefaultFilteringParamsForm,):
    employer = Employer.objects.get(user__exact = request.user)
    
    if request.method == 'POST':
        form = form_class(data=request.POST,
                          instance = employer)
        if form.is_valid():

            form.save()
            employer.automatic_filtering_setup_completed = True
            employer.save()
            return HttpResponse(simplejson.dumps({"valid":True}))
        return HttpResponse(simplejson.dumps({"valid":False}))
    else:
        form = form_class(instance=employer)
    data = {
        'form':form
    }
    return render_to_response(template_name,
                              data,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_event(request, template_name="employer/employer_event.html"):
    employer = Employer.objects.get(user__exact = request.user)
    
    data = {
    'employer':employer,
    }
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_events(request, template_name="employer/employer_events.html"):

    employer = Employer.objects.get(user__exact = request.user)

    data = {
            'upcoming_events':employer.events.filter(datetime__gt=datetime.datetime.now()),
            'user': employer.company_name,
            }   
    return render_to_response(template_name, data, context_instance=RequestContext(request))

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
def employer_filtering_results(request, template_name='employer_results.html'):

    if request.method == "POST":
        
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

        """
        if request.GET.has_key('courses[]'):
            filtering_results = filtering_results.filter(Q(first_major__name__in=request.GET.getlist('courses[]')) | Q(second_major__name__in=request.GET.getlist('courses[]'))).order_by("-last_updated")
        """
        
        
        # We have a search query too, so do that and then only keep the ones
        # that were also in the filtering results.
        if request.POST['query'] != 'null':
            sqs= SearchQuerySet().filter(content=request.POST['query'])
            results = []
            if request.POST['ordering'] == "relevancy":
                for student in sqs:
                    if student.object in filtering_results:
                        results.append(student.object)
            else:
                array_of_ids = [student.objectid for student in sqs]
                results = filtering_results.filter(id__in=array_of_ids)
        else:
            if request.POST['ordering'] == "relevancy":
                results = list(filtering_results.order_by('last_updated'))*100
            else:
                results = filtering_results.order_by(request.POST['ordering'])
        
        """
        for student in results:
            student.results_count += 1
            student.save()
        """
        paginator = DiggPaginator(results, int(request.POST['results_per_page']), body=5, padding=1, margin=2) 

        data = {} 
        data['page'] = paginator.page(request.POST['page'])

        return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_employer, login_url=settings.LOGIN_URL)
def employer_filtering(request, template_name='employer_filtering.html'):
    
    data = {}
    data['user'] = Employer.objects.get(user = request.user)
    data['filtering_form'] = FilteringForm(initial={'ordering': data['user'].default_student_ordering, 'results_per_page' : data['user'].results_per_page})
    data['search_form'] = SearchForm()
    data['cart'] = request.session.get('cart', {})
    
    form = SearchForm(data=request.POST)
    if request.method == "POST" and request.POST.has_key('query') and form.is_valid():
        form.clean()
        data['query'] = form.cleaned_data['query']
    return render_to_response(template_name, data, context_instance=RequestContext(request))
    
    """
    if request.is_ajax():
        if cache.get('page') and (int(cache.get('page')) == int(request.GET['page'])+1 or int(cache.get('page')) == int(request.GET['page'])-1):
            results = cache.get('results')
            cache.set('page', request.GET['page'], 300)
        else:
            all_students = Student.objects.all()
    
            # Building up initial filtering query.
            kwargs = {}
            if request.GET['gpa'] != "0":
                kwargs['gpa__gte'] = request.GET['gpa']
            if request.GET['act'] != "0":
                kwargs['act__gte'] = request.GET['act']
            if request.GET['sat_t'] != "600":
                kwargs['sat_t__gte'] = request.GET['sat_t']
            if request.GET['sat_m'] != "200":
                kwargs['sat_m__gte'] = request.GET['sat_m']
            if request.GET['sat_v'] != "200":
                kwargs['sat_v__gte'] = request.GET['sat_v']
            if request.GET['sat_w'] != "200":
                kwargs['sat_w__gte'] = request.GET['sat_w']
    
            # As of now, we order-by "last_updated" most recent first.
            # Might want to add in more ordering options later on.
            filtering_results = all_students.filter(**kwargs).order_by("-last_updated")
    
            # The courses filtering is a bit more complex and thus done separately.
            # I would want to integrate this with the other lazy query building
            # if I need the filtering to appear faster.
            if request.GET.has_key('courses[]'):
                filtering_results = filtering_results.filter(Q(first_major__name__in=request.GET.getlist('courses[]')) | Q(second_major__name__in=request.GET.getlist('courses[]'))).order_by("-last_updated")
    
            # We have a search query too, so do that and then only keep the ones
            # that were also in the filtering results.
            if request.GET['query'] != '':
                sqs= SearchQuerySet().filter(content=request.GET['query'])
                results = []
                for student in sqs:
                    if student.object in filtering_results:
                        results.append(student.object)
    
            # If no search query, then filtering_results are the actual results
            else:
                results = list(filtering_results)
            cache.delete('results')
            cache.delete('page')
            cache.set('results', results, 300)
            cache.set('page', request.GET['page'], 300)
        
        paginator = Paginator(results, settings.RESULTS_PER_PAGE)

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
            
        try:
            result_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            result_page = paginator.page(paginator.num_pages)

        for student in result_page.object_list:
            student.resultsCount += 1
            student.save()

        return HttpResponse(simplejson.dumps({'results':result_page.object_list, \
                                'has_previous': result_page.has_previous(),\
                              'prev_index': result_page.previous_page_number(),\
                              'has_next': result_page.has_next(),\
                              'next_index': result_page.next_page_number(),\
                              'total_count' : result_page.paginator.count,\
                              'start_index': result_page.start_index(),\
                              'end_index': result_page.end_index()}, cls=ModelAwareJSONEncoder), mimetype="application/json")
    else:
        #cache.delete('results')
        #cache.delete('page')
        data = {}
        data['per_page'] = settings.RESULTS_PER_PAGE
        data['user'] = Employer.objects.get(user = request.user)
        data['graduation_years'] = list(GraduationYear.objects.all())
        data['school_years'] = list(SchoolYear.objects.all())
        data['prev_employers'] = list(Employer.objects.all())
        data['industries'] = list(Industry.objects.all())
        data['languages'] = list(Language.objects.all())
        data['courses'] = Course.objects.all()
        data['campus_orgs'] = campus_org_types_as_choices()
        data['cart'] = request.session.get('cart', {})
        if request.POST.has_key('query'):
            form = SearchForm(data=request.POST)
            if form.is_valid():
                form.clean()
                results = []
                sqs = SearchQuerySet().suma_query(form.cleaned_data['query'])
                # We want to return a QuerySet, not a SearchQuerySet
                # Is there a faster way to do this?
                for result in sqs:
                    results.append(result.object)
                paginator = Paginator(results, settings.RESULTS_PER_PAGE)
                try:
                    result_page = paginator.page(1)
                except (EmptyPage, InvalidPage):
                    result_page = paginator.page(paginator.num_pages)
                data['query'] = form.cleaned_data['query']
                data['result_page'] = result_page
                return render_to_response(template_name, data, context_instance=RequestContext(request))
        else:
            paginator = Paginator(list(Student.objects.order_by("-last_updated")), settings.RESULTS_PER_PAGE)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                result_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                result_page = paginator.page(paginator.num_pages)
            data['result_page'] = result_page
            return render_to_response(template_name, data, context_instance=RequestContext(request))
    """
    """
            paginator = Paginator(list(Student.objects.order_by("-last_updated")), settings.RESULTS_PER_PAGE)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                result_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                result_page = paginator.page(paginator.num_pages)
            data['result_page'] = result_page
            return render_to_response(template_name, data, context_instance=RequestContext(request))
    """
    """
        if request.POST.has_key('query'):
            if form.is_valid():
                form.clean()
                results = []
                sqs = SearchQuerySet().suma_query(form.cleaned_data['query'])
                # We want to return a QuerySet, not a SearchQuerySet
                # Is there a faster way to do this?
                for result in sqs:
                    results.append(result.object)
                paginator = Paginator(results, settings.RESULTS_PER_PAGE)
                try:
                    result_page = paginator.page(1)
                except (EmptyPage, InvalidPage):
                    result_page = paginator.page(paginator.num_pages)
                data['query'] = form.cleaned_data['query']
                data['result_page'] = result_page
                return render_to_response(template_name, data, context_instance=RequestContext(request))
        """
"""
    if request.GET.has_key('school_year'):
        kwargs['school_year__in'] = request.GET.getlist('school_year')
    if request.GET.has_key('graduation_year'):
        kwargs['graduation_year__in'] = request.GET.getlist('graduation_year')

    if request.GET.has_key('living_group'):
        kwargs['living_group__in'] = request.GET.getlist('living_group')
    if request.GET.has_key('citizen'):
        kwargs['citizen__exact'] = True
    if request.GET.has_key('ofage'):
        kwargs['older_than_18__exact'] = True
               if request.GET.has_key('activities'):
        profiles = profiles.filter(activities__name__in=[activity.objects.get(id__exact = x).name for x in request.GET.getlist('activities')]).distinct()

    if request.method == "POST":
        for profile in profiles:
            profile.resumeCount += 1
            profile.save()
        resumeNames = ""
        postData =  request.POST.lists()
        for i in postData[0][1]:
            resumeNames += " media/" + str(profiles[int(i)].resume)
        pdfName = str(request.session['employer']).replace(" ", "_") + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        p = subprocess.Popen("pdftk.exe" + resumeNames + " cat output media/resumes/"+ pdfName +".pdf", shell=True)
        p.wait()
        return HttpResponseRedirect('/media/resumes/' + pdfName + '.pdf')
"""