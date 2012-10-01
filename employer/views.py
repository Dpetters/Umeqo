from __future__ import division
from __future__ import absolute_import

import cStringIO
import os
import re
import zipfile

from datetime import datetime
from haystack.query import SearchQuerySet, SQ
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files import File
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.contrib.sites.models import get_current_site
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.http import require_POST, require_GET

from core import messages, enums as core_enums
from core.decorators import render_to
from core.digg_paginator import DiggPaginator
from core.email import get_basic_email_context, send_email
from core.file_utils import find_first_file
from core.http import Http403, Http400
from core.management.commands.zip_resumes import zip_resumes
from core.models import Industry
from core.search import search
from core.templatetags.filters import format_unix_time
from employer import enums as employer_enums
from employer.decorators import has_at_least_premium, is_recruiter
from employer.forms import CreateEmployerForm, EmployerProfileForm, RecruiterForm, \
                           RecruiterPreferencesForm, StudentFilteringForm, StudentSearchForm, \
                           DeliverResumeBookForm
from employer.models import ResumeBook, Recruiter, Employer, EmployerStudentComment
from employer.view_helpers import employer_search_helper, process_results, get_resume_book_size, \
                                  order_results, get_unlocked_students
from events.models import Event
from events.view_helpers import get_employer_upcoming_events_context
from registration.forms import PasswordChangeForm
from student import enums as student_enums
from student.decorators import is_student
from student.models import Student
from subscription.utils import sum_charges, get_charges


@require_GET
@render_to("employer_logo.html")
def employer_logo(request):
    if not request.GET.has_key("employer_name"):
        raise Http400("Request GET is missing the employer_name.")
    name = request.GET['employer_name']
    try:
        e = Employer.objects.get(name=name)
    except:
        raise Http404("Employer with name %s does not exist" % name)
    return {'employer': e}

    
@require_GET
@user_passes_test(is_recruiter)
@render_to("employer_account.html")
def employer_account(request, preferences_form_class = RecruiterPreferencesForm, 
                     change_password_form_class = PasswordChangeForm,
                     extra_context=None):
    context = {}
    recruiter = request.user.recruiter
    context['recruiter'] = recruiter
    employer = recruiter.employer
    context['employer'] = employer
    customer = request.META['customer']
    has_at_least_premium = request.META['has_at_least_premium']
    context['customer'] = customer
    subscription = customer.subscription
    if subscription:
        context['current_period_end'] =  format_unix_time(customer.subscription.current_period_end)
    msg = request.GET.get('msg', None)
    if msg:
        page_messages = {
            'payment-changed': messages.payment_changed,
            'password-changed': messages.password_changed,
            'subscription-cancelled' : messages.subscription_cancelled,
            'upgraded_to_premium' : messages.upgraded_to_premium,
            'changed_billing' : messages.changed_billing
        }
        if page_messages.has_key(msg):
            context["msg"] = page_messages[msg]
    context['other_recruiters'] = employer.recruiter_set.exclude(id=recruiter.id)
    context['preferences_form'] = preferences_form_class(instance=recruiter.recruiterpreferences)
    context['change_password_form'] = change_password_form_class(request.user)
    charges = get_charges(customer.id)
    context['charges'] = charges
    context['charge_total'] = sum_charges(charges)
    context['max_users_for_basic_users'] = s.MAX_USERS_FOR_BASIC_USERS
    context['can_create_more_accounts'] = has_at_least_premium or len(Recruiter.objects.filter(employer=employer)) < s.MAX_USERS_FOR_BASIC_USERS
    context.update(extra_context or {})
    return context


@render_to("employer_new.html")
def employer_new(request, form_class=CreateEmployerForm, extra_context=None):
    if not (request.user.is_authenticated() and hasattr(request.user, "campusorg") or hasattr(request.user, "student")):
        raise Http403("You must be logged in.")
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            new_employer = form.save()
            recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
            
            context = Context({'first_name':request.user.first_name,
                               'last_name': request.user.last_name,
                               'email':request.user.email,
                               'new_employer':new_employer,
                               'new_employer_industries':" ".join(map(lambda x: x.name, new_employer.industries.all()))})
            context.update(get_basic_email_context())
             
            body = render_to_string('employer_new_email_body.txt', context)
                                    
            subject = ''.join(render_to_string('email_admin_subject.txt', {
                'message': "New Employer: %s" % new_employer 
            }, context).splitlines())
                            
            send_email(subject, body, recipients)
            
            data = {"name": new_employer.name, "id": new_employer.id}
        else:
            data = {'errors': form.errors }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class()
    context = {'form': form }
    context.update(extra_context or {}) 
    return context


@user_passes_test(lambda x: is_student(x) or is_recruiter(x))
@render_to("employer_profile_preview.html")
def employer_profile_preview(request, slug, extra_context=None):
    try:
        employer = Employer.objects.get(slug=slug)
    except Employer.DoesNotExist:
        raise Http404("Employer with slug %s does not exist" % slug)
    if is_student(request.user):
        return HttpResponseRedirect("%s?id=%s" % (reverse("employers"), employer.id))
    elif is_recruiter(request.user):
        context = {'employer':employer}
        context.update(get_employer_upcoming_events_context(employer, request.user))
        context.update(extra_context or {})
        return context


@user_passes_test(is_recruiter)
@render_to("employer_recruiter_new.html")
def employer_recruiter_new(request, form_class=RecruiterForm, extra_context=None):
    employer = request.user.recruiter.employer
    has_at_least_premium = request.META['has_at_least_premium']
    recruiter_num = len(Recruiter.objects.filter(employer=employer))
    if not has_at_least_premium and recruiter_num >= s.MAX_USERS_FOR_BASIC_USERS:
        raise Http403("In order to create more than %d accounts for your firm, you must subscribe to a paid plan." % (s.MAX_USERS_FOR_BASIC_USERS))
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if len(user.email)>30:
                username = user.email.split("@")[0]
                if len(username) > 30:
                    username = username[:30]
            else:
                username = user.email
            user.username = username
            user.save()
            form.save_m2m()
            Recruiter.objects.create(user = user, employer = request.user.recruiter.employer)
            data = {}
        else:
            data = {'errors': form.errors }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class()
    context = {'form': form }
    context.update(extra_context or {}) 
    return context


@user_passes_test(is_recruiter)
@render_to("employer_account_delete.html")
def employer_account_delete(request):
    if request.user.recruiter.employer.recruiter_set.exclude(id=request.user.recruiter.id).exists():
        if request.method == "POST":
            for sk in request.user.sessionkey_set.all():
                Session.objects.filter(session_key=sk.session_key).delete()
            request.user.sessionkey_set.all().delete()
            request.user.recruiter.delete()
            request.user.delete()
            return HttpResponse()
        else:
            context = {}
            return context
    else:
        raise Http403("You cannot delete your account when you are the only recruiter with credentials for Umeqo.") 


@user_passes_test(is_recruiter)
@render_to("employer_resume_book_delete.html")
def employer_resume_book_delete(request, extra_context = None):
    if request.method == "POST":
        if not request.POST.has_key("resume_book_id"):
            raise Http400("Request POST is missing the resume_book_id.")
        try:
            ResumeBook.objects.get(id=request.POST["resume_book_id"]).delete()
        except ResumeBook.DoesNotExist:
            raise Http404("No resume book exists with id of %s" % request.POST["resume_book_id"])
        return HttpResponse()
    else:
        context = {}
        context.update(extra_context or {})
        return context


@user_passes_test(is_recruiter)
@require_GET
@render_to("employer_other_recruiters.html")
def employer_other_recruiters(request):
    context = {'other_recruiters':request.user.recruiter.employer.recruiter_set.exclude(id=request.user.recruiter.id)}
    return context


@user_passes_test(is_recruiter)
@require_POST
def employer_account_preferences(request, form_class=RecruiterPreferencesForm):
    form = form_class(data=request.POST, instance=request.user.recruiter.recruiterpreferences)
    data = []
    if form.is_valid():
        request.user.recruiter.recruiter_preferencess = form.save()
    else:
        data = {'errors': form.errors }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@user_passes_test(is_recruiter)
@render_to("employer_profile.html")
def employer_profile(request, form_class=EmployerProfileForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.recruiter.employer)
        data = []
        if form.is_valid():
            employer = form.save()
            # Update index
            employer.save()
        else:
            data = {'errors': form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    else:
        context = {'form':form_class(instance=request.user.recruiter.employer),
                   'max_industries':s.EP_MAX_INDUSTRIES,
                   'edit':True}
        context.update(extra_context or {})
        return context


@user_passes_test(is_recruiter)
@require_POST
def employer_student_toggle_star(request):
    if not request.POST.has_key('student_id'):
        raise Http400("Request POST is missing the student_id.")
    student = Student.objects.get(id=request.POST['student_id'])
    if student in request.user.recruiter.employer.starred_students.all():
        request.user.recruiter.employer.starred_students.remove(student)
        data = {'action':employer_enums.UNSTARRED}
    else:
        request.user.recruiter.employer.starred_students.add(student)
        data = {'action':employer_enums.STARRED}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@require_POST
@user_passes_test(is_recruiter)
def employer_students_add_star(request):
    if not request.POST.has_key('student_ids'):
        raise Http400("Request POST is missing student_ids.")
    for id in request.POST['student_ids'].split('~'):
        student = Student.objects.get(id=id)  
        if student not in request.user.recruiter.employer.starred_students.all():
            request.user.recruiter.employer.starred_students.add(student)
    return HttpResponse()


@user_passes_test(is_recruiter)
@require_POST
def employer_students_remove_star(request):
    if not request.POST.has_key('student_ids'):
        raise Http400("Request POST is missing the student_ids.")
    for id in request.POST['student_ids'].split('~'):
        student = Student.objects.get(id=id)  
        if student in request.user.recruiter.employer.starred_students.all():
            request.user.recruiter.employer.starred_students.remove(student)
    return HttpResponse()


@user_passes_test(is_recruiter)
@require_POST
def employer_student_comment(request):
    if not request.POST.has_key('student_id'):
        raise Http400("Request POST is missing the student_id")
    if not request.POST.has_key('comment'):
        raise Http400("Request POST is missing the comment.")
    student = Student.objects.get(id=request.POST['student_id'])
    comment = request.POST['comment']
    try:
        student_comment = EmployerStudentComment.objects.get(student=student, employer=request.user.recruiter.employer)
    except EmployerStudentComment.DoesNotExist:
        EmployerStudentComment.objects.create(employer = request.user.recruiter.employer, student=student, comment=comment)
    else:
        student_comment.comment = comment
        student_comment.save()
    return HttpResponse()


@user_passes_test(is_recruiter)
@require_POST
def employer_resume_book_toggle_student(request):
    if not request.POST.has_key('student_id'):
        raise Http400("Request POST is missing the student_id.")
    student = Student.objects.get(id=request.POST['student_id'])
    try:
        resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
    data = {}
    if student in resume_book.students.visible():
        resume_book.students.remove(student)
        data['action'] = employer_enums.REMOVED
    else:
        employer = request.user.recruiter.employer
        if student in get_unlocked_students(employer, request.META['has_at_least_premium']):
            if len(resume_book.students.visible()) >= s.RESUME_BOOK_CAPACITY:
                raise Http403("You already have the max number (%d) of allowed students in you resumebook!" % (s.RESUME_BOOK_CAPACITY))
            resume_book.students.add(student)
            if not request.user.recruiter.employer.name != "Umeqo":
                student.studentstatistics.add_to_resumebook_count += 1
                student.studentstatistics.save()
            data['action'] = employer_enums.ADDED
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@user_passes_test(is_recruiter)
@require_POST
def employer_resume_book_add_students(request):
    if not request.POST.has_key('student_ids'):
        raise Http400("Request POST is missing the student_ids.")
    try:
        resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
        if len(resume_book.students.visible()) >= s.RESUME_BOOK_CAPACITY:
            raise Http403("You already have the max number (%d) of allowed students in you resumebook!" % (s.RESUME_BOOK_CAPACITY))
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
    employer = request.user.recruiter.employer
    unlocked_students = get_unlocked_students(employer, request.META['has_at_least_premium'])
    if request.POST['student_ids']:
        for id in request.POST['student_ids'].split('~'):
            student = Student.objects.get(id=id)
            if student in unlocked_students:
                if student not in resume_book.students.visible():
                    resume_book.students.add(student)
                if not request.user.recruiter.employer.name != "Umeqo":
                    student.studentstatistics.add_to_resumebook_count += 1
                    student.studentstatistics.save()
    return HttpResponse()


@user_passes_test(is_recruiter)
@require_POST
def employer_resume_book_remove_students(request):
    if not request.POST.has_key('student_ids'):
        raise Http400("Request is missing the student_ids.")
    try:
        resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
    if request.POST['student_ids']:
        for student_id in request.POST['student_ids'].split('~'):
            student = Student.objects.get(id=student_id)  
            if student in resume_book.students.visible():
                resume_book.students.remove(student)
    return HttpResponse()


@require_GET
@user_passes_test(is_recruiter)
@render_to('employer_student_attendance.html')
def employer_student_event_attendance(request):
    if not request.GET.has_key('student_id'):
        raise Http400("Request GET is missing the student_id.")
    context={}
    student = Student.objects.visible().get(id=request.GET['student_id'])
    context['events'] = request.user.recruiter.employer.events_attending.filter(attendee__student=student)
    context['student'] = student
    return context


@user_passes_test(is_recruiter)
@require_GET
@render_to("employer_resume_book_history.html")
def employer_resume_book_history(request, extra_context=None):
    context = {"resume_books":request.user.recruiter.resumebook_set.filter(delivered=True),
               'email_delivery_type': core_enums.EMAIL}
    context.update(extra_context or {})
    return context


@has_at_least_premium
@user_passes_test(is_recruiter)
def employer_resumes_download(request, extra_context=None):
    file_path = find_first_file(s.MEDIA_ROOT, "%s.*.zip" % s.ALL_ZIPPED_RESUMES_FILENAME_START)
    if file_path:
        mimetype = "application/zip"
        response = HttpResponse(file(file_path, "rb").read(), mimetype=mimetype)
        filename = file_path.split("/")[-1]
        response["Content-Disposition"] = 'attachment; filename="%s.zip"' % filename
        return response
    else:
        zip_resumes()
        return employer_resumes_download(request)


@user_passes_test(is_recruiter)
@require_GET
@render_to()
def employer_students(request, extra_context=None):
    context = {}
    if request.is_ajax():
        student_list = request.GET['student_list']
        student_list_id = request.GET['student_list_id']
        recruiter = request.user.recruiter
        if student_list == student_enums.GENERAL_STUDENT_LISTS[0][1]:
            students = SearchQuerySet().models(Student).filter(visible=True)
        else:
            if student_list == student_enums.GENERAL_STUDENT_LISTS[1][1]:
                students = get_unlocked_students(recruiter.employer, request.META['has_at_least_premium'])
            elif student_list == student_enums.GENERAL_STUDENT_LISTS[2][1]:
                students = recruiter.employer.starred_students.all()
            elif student_list == student_enums.GENERAL_STUDENT_LISTS[3][1]:
                try:
                    resume_book = ResumeBook.objects.get(recruiter = recruiter, delivered=False)
                except ResumeBook.DoesNotExist:
                    resume_book = ResumeBook.objects.create(recruiter = recruiter)
                students = resume_book.students.visible()
            else:
                parts = student_list.split(" ")
                if parts[-1] == "RSVPs" or parts[-1] == "Attendees" or parts[-1] == "Drop" and parts[-2] == "Resume":
                    try:
                        e = Event.objects.get(id = student_list_id)
                    except:
                        raise Http404
                    if parts[-1] == "RSVPs":
                        students = Student.objects.visible().filter(rsvp__in=e.rsvp_set.filter(attending=True), profile_created=True)
                    elif parts[-1] == "Attendees":
                        students = Student.objects.visible().filter(attendee__in=e.attendee_set.all(), profile_created=True)
                    elif parts[-1] == "Drop" and parts[-2] == "Resume":
                        students = Student.objects.visible().filter(droppedresume__in=e.droppedresume_set.all(), profile_created=True)
                else:
                    students = ResumeBook.objects.get(id = student_list_id).students.visible()
            students = SearchQuerySet().models(Student).filter(obj_id__in = [student.id for student in students])
        am_filtering = False
        if request.GET.has_key('gpa'):
            am_filtering = True
            students = students.filter(gpa__gte = request.GET['gpa'])

        if request.GET.has_key('act'):
            am_filtering = True
            students = students.filter(act__gte = request.GET['act'])

        if request.GET.has_key('sat_t'):
            am_filtering = True            
            students = students.filter(sat_t__gte = request.GET['sat_t'])

        if request.GET.has_key('sat_m'):
            am_filtering = True            
            students = students.filter(sat_m__gte = request.GET['sat_m'])
            
        if request.GET.has_key('sat_v'):
            am_filtering = True            
            students = students.filter(sat_v__gte = request.GET['sat_v'])

        if request.GET.has_key('sat_w'):
            am_filtering = True            
            students = students.filter(sat_w__gte = request.GET['sat_w'])

        if request.GET.has_key('degree_programs'):
            am_filtering = True
            students = students.filter(degree_program__in = request.GET['degree_programs'].split('~'))

        if request.GET.has_key('graduation_years'):
            am_filtering = True            
            students = students.filter(graduation_year__in = request.GET['graduation_years'].split('~'))

        if request.GET.has_key('employment_types'):
            am_filtering = True            
            students = students.filter(looking_for__in = request.GET['employment_types'].split('~'))

        if request.GET.has_key('previous_employers'):
            am_filtering = True            
            students = students.filter(previous_employers__in = request.GET['previous_employers'].split('~'))

        if request.GET.has_key('industries_of_interest'):
            am_filtering = True            
            students = students.filter(industries_of_interest__in = request.GET['industries_of_interest'].split('~'))
    
        if request.GET.has_key('languages'):
            am_filtering = True            
            students = students.filter(languages__in = request.GET['languages'].split('~'))

        if request.GET.has_key('campus_orgs'):
            am_filtering = True            
            students = students.filter(campus_involvement__in = request.GET['campus_orgs'].split('~'))

        if request.GET.has_key('countries_of_citizenship'):
            am_filtering = True            
            students = students.filter(countries_of_citizenship__in =  request.GET['countries_of_citizenship'].split('~'))
            
        if request.GET['older_than_21'] != 'N':
            am_filtering = True
            students = students.filter(older_than_21 = True)

        if request.GET.has_key('courses'):
            am_filtering = True
            courses = request.GET['courses'].split('~')
            students = students.filter(SQ(first_major__in = courses)|SQ(second_major__in = courses))

        if request.GET.has_key('query'):
            students = search(students, request.GET['query'])
            # Highlight the results
            students = students.highlight()

        results_per_page = int(request.GET['results_per_page'])
        start_index = results_per_page * (int(request.GET['page']) - 1)
        count = students.count()

        if start_index >= count:
            start_index = 0
        
        ordered_results = order_results(students, request)[start_index:start_index + results_per_page]
        ordered_result_objects = []
        for search_result in ordered_results:
            if search_result.highlighted:
                ordered_result_object = (search_result.object,  search_result.highlighted['text'][0])
            else:
                ordered_result_object = (search_result.object,  "")
            ordered_result_objects.append(ordered_result_object)
        padded_ordered_results = ['']*count

        for i in range(len(ordered_result_objects)):
            padded_ordered_results[i + start_index] = ordered_result_objects[i]
        
        paginator = DiggPaginator(padded_ordered_results, results_per_page, body=3, padding=1, margin=2)
        context['filtering'] = am_filtering

        try:
            page = paginator.page(request.GET['page'])
        except EmptyPage:
            page = paginator.page(1)
        
        context['page'] = page
        context['results'] = process_results(request.user.recruiter, request.META['has_at_least_premium'], page)
        context['current_student_list'] = request.GET['student_list']
        context['total_results_num'] = count

        # I don't like this method of statistics
        if request.user.recruiter.employer.name != "Umeqo":
            for student, highlighted_text, is_in_resume_book, is_starred, comment, num_of_events_attended, visible in context['results']:
                student.studentstatistics.shown_in_results_count += 1
                student.studentstatistics.save()

        resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
        if len(resume_book.students.visible()) >= s.RESUME_BOOK_CAPACITY:
            context['resume_book_capacity_reached'] = True

        context['TEMPLATE'] = 'employer_students_results.html'
        context.update(extra_context or {}) 
        return context
    else:
        page_messages = {
            'NO_STUDENTS_SELECTED_MESSAGE': messages.no_students_selected,
            'WAIT_UNTIL_RESUME_BOOK_IS_READY_MESSAGE': messages.wait_until_resume_book_is_ready
        }
        context['page_messages'] = page_messages
        context['query'] = request.GET.get('query', '')

        # Passing the employer id to generate tha appropriate student list choices
        context['student_filtering_form'] = StudentFilteringForm(initial={
                'has_at_least_premium':request.META['has_at_least_premium'],
                'recruiter_id': request.user.recruiter.id,
                'ordering': request.user.recruiter.recruiterpreferences.default_student_result_ordering,                           
                'results_per_page': request.user.recruiter.recruiterpreferences.default_student_results_per_page
        })
        context['student_search_form'] = StudentSearchForm()
        context['added'] = employer_enums.ADDED
        context['starred'] = employer_enums.STARRED
        context['email_delivery_type'] = core_enums.EMAIL
        context['in_resume_book_student_list'] = student_enums.GENERAL_STUDENT_LISTS[3][1]
        context['resume_book_capacity'] = s.RESUME_BOOK_CAPACITY
    context['TEMPLATE'] = 'employer_students.html'
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
@render_to('employer_resume_book_summary.html')
def employer_resume_book_summary(request, extra_context=None):
    try:
        resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
    except ResumeBook.MultipleObjectsReturned:
        resume_books = ResumeBook.objects.filter(recruiter=request.user.recruiter, delivered=False)
        for i, rb in enumerate(resume_books):
            if i != 0:
                rb.delete()
            else:
                resume_book = rb
    resume_book_capacity = s.RESUME_BOOK_CAPACITY
    student_num = len(resume_book.students.visible())
    float_percentage = min(student_num, resume_book_capacity)/float(resume_book_capacity)*100
    context = {'student_num': student_num,
               'float_percentage':float_percentage,
               'int_precentage':int(float_percentage),
               'resume_book_capacity': resume_book_capacity}
    context.update(extra_context or {}) 
    return context


@require_GET
@user_passes_test(is_recruiter)
@render_to('employer_resume_book_deliver.html')
def employer_resume_book_deliver(request, form_class=DeliverResumeBookForm, extra_context=None):
    context = {'form':form_class(initial={'emails':request.user.email})}
    if not request.GET.has_key("resume_book_id"):
        raise Http400("Request GET is missing the resume_book_id.")
    if request.GET["resume_book_id"]:
        try:
            resume_book = ResumeBook.objects.get(id=request.GET["resume_book_id"])
        except ResumeBook.DoesNotExist:
            raise Http400("No resume book exists with id of %s" % request.GET["resume_book_id"])
    else:
        try:
            resume_book = ResumeBook.objects.get(recruiter=request.user.recruiter, delivered=False)
        except ResumeBook.DoesNotExist:
            raise Http400("There isn't a resume book ready to be delivered.")
    resume_book_size = get_resume_book_size(resume_book)
    context['resume_book'] = resume_book
    context['resume_book_size'] = resume_book_size
    context['max_resume_book_size_as_attachment'] = s.RESUME_BOOK_MAX_SIZE_AS_ATTACHMENT
    if resume_book_size > s.RESUME_BOOK_MAX_SIZE_AS_ATTACHMENT:
        context['disable_email_delivery'] = True
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
@require_POST
def employer_resume_book_create(request):
    if request.POST.has_key("resume_book_id") and request.POST['resume_book_id']:
        redelivering = True
        try:
            resume_book = ResumeBook.objects.get(id=request.POST["resume_book_id"])
        except ResumeBook.DoesNotExist:
            raise Http404("No resume book exists with id of %s" % request.POST["resume_book_id"])
    else:
        redelivering = False
        try:
            resume_book, created = ResumeBook.objects.get_or_create(recruiter = request.user.recruiter, delivered=False)    
        except ResumeBook.MultipleObjectsReturned:
            resume_books = ResumeBook.objects.filter(recruiter=request.user.recruiter, delivered=False)
            for i, rb in enumerate(resume_books):
                if i != 0:
                    rb.delete()
                else:
                    resume_book = rb

    if redelivering:
        resume_book_name = resume_book.name
    else:
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        resume_book_name = "%s_%s" % (str(request.user), now,)
        resume_book.name = resume_book_name
        resume_book.save()

    file_path = "%semployer/resumebook/"% (s.MEDIA_ROOT,)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    if request.POST['delivery_format'] == 'separate':
        # Create the zip file
        file_name = "%s%s.zip" % (file_path, resume_book_name,)
        output = zipfile.ZipFile(file_name, 'w')
        for student in resume_book.students.visible():
            resume_file = file("%s%s" % (s.MEDIA_ROOT, str(student.resume)), "rb")
            name = "%s %s (%s, %s).pdf" % (student.first_name, student.last_name, student.graduation_year, student.degree_program)
            output.write(resume_file.name, name, zipfile.ZIP_DEFLATED)
        resume_file.close()
        output.close()
    else:
        file_name = "%s%s.pdf" % (file_path, resume_book_name)
        report_buffer = cStringIO.StringIO() 
        c = Canvas(report_buffer)  
        now = datetime.now()
        first_line = "Created on %s at %s" % (now.strftime('%m/%d/%Y'), now.strftime('%I:%M %p'))
        c.drawString(1*cm, 28.5*cm, first_line)
        c.drawString(1*cm, 28*cm, str(request.user.recruiter))
        c.drawString(1*cm, 27.5*cm, str(request.user.recruiter.employer))
        c.drawString(16*cm, 28.5*cm, "Created using Umeqo")
        c.drawString(8.5*cm, 26.5*cm, "Resume Book Contents")
        for page_num, student in enumerate(resume_book.students.visible().order_by("graduation_year", "first_name", "last_name")):
            c.drawString(6.5*cm, (25.5-page_num*.5)*cm, "%s %s" % (student.first_name, student.last_name))
            c.drawString(12*cm, (25.5-page_num*.5)*cm,  "%s, %s" %(student.graduation_year, student.degree_program))
        c.showPage()
        c.save()
        output = PdfFileWriter()
        output.addPage(PdfFileReader(cStringIO.StringIO(report_buffer.getvalue())).getPage(0)) 
        for student in resume_book.students.visible().order_by("graduation_year", "first_name", "last_name"):
            resume_file = open("%s%s" % (s.MEDIA_ROOT, str(student.resume)), "rb")
            resume = PdfFileReader(resume_file)
            if resume.getIsEncrypted():
                resume.decrypt("")
            for page in range(resume.getNumPages()):
                output.addPage(resume.getPage(page))
        outputStream = file(file_name, "wb")
        output.write(outputStream)
        outputStream.close()
        resume_file.close()

    resume_book_contents = open(file_name, "rb")
    resume_book.resume_book.save(file_name, File(resume_book_contents))
    resume_book_contents.close()
    return HttpResponse()


@require_POST
@user_passes_test(is_recruiter)
@render_to("employer_resume_book_delivered.html")
def employer_resume_book_email(request, extra_context=None):
    if not request.POST.has_key('emails'):
        raise Http400("Request POST is missing the emails.")
    if request.POST.has_key("resume_book_id") and request.POST['resume_book_id']:
        redelivering = True
        try:
            resume_book = ResumeBook.objects.get(id=request.POST["resume_book_id"])
        except ResumeBook.DoesNotExist:
            raise Http404("No resume book exists with id of %s" % request.POST["resume_book_id"])
    else:
        redelivering = False
        try:
            resume_book, created = ResumeBook.objects.get_or_create(recruiter = request.user.recruiter, delivered=False)
        except ResumeBook.MultipleObjectsReturned:
            resume_books = ResumeBook.objects.filter(recruiter=request.user.recruiter, delivered=False)
            for i, rb in enumerate(resume_books):
                if i != 0:
                    rb.delete()
                else:
                    resume_book = rb
    reg = re.compile(r"\s*[;, \n]\s*")
    recipients = reg.split(request.POST['emails'])
    site = get_current_site(request)
    subject = "[%s] Resume Book Delivery" % (site.name)
    f = open("%s%s" % (s.MEDIA_ROOT, resume_book.resume_book.name), "rb")
    content = f.read()
    if request.POST.has_key('name') and request.POST['name']:
        filename = request.POST['name']
    else:
        filename = os.path.basename(resume_book.name)

    context = get_basic_email_context()
    context['deliverer_fullname'] = "%s %s" % (request.user.first_name, request.user.last_name)
    context['deliverer_email'] = request.user.email

    for recipient in recipients:
        context['first_name'] = recipient.split("@")[0]
        text_email_body = render_to_string('resume_book_email_body.txt', context)
        html_email_body = render_to_string('resume_book_email_body.html', context)
        send_email(subject, text_email_body, recipients, html_email_body, "%s.pdf" % (filename), content, "application/pdf")
    if redelivering:
        resume_book.last_updated = datetime.now()
    else:
        resume_book.name = filename
        resume_book.delivered = True
    resume_book.save()
    context = {}
    context.update(extra_context or {})
    return context


@require_GET
@user_passes_test(is_recruiter)
def employer_resume_book_download(request):
    if request.GET.has_key("resume_book_id") and request.GET['resume_book_id']:
        redelivering = True
        try:
            resume_book = ResumeBook.objects.get(id=request.GET["resume_book_id"])
        except ResumeBook.DoesNotExist:
            raise Http404("No resume book exists with id of %s" % request.GET["resume_book_id"])
    else:
        redelivering = False
        try:
            resume_book, created = ResumeBook.objects.get_or_create(recruiter = request.user.recruiter, delivered=False)
        except ResumeBook.MultipleObjectsReturned:
            resume_books = ResumeBook.objects.filter(recruiter=request.user.recruiter, delivered=False)
            for i, rb in enumerate(resume_books):
                if i != 0:
                    rb.delete()
                else:
                    resume_book = rb
    if request.GET['delivery_format'] == 'separate':
        mimetype = "application/zip"
    else:
        mimetype = "application/pdf"
    response = HttpResponse(file("%s%s" % (s.MEDIA_ROOT, resume_book.resume_book), "rb").read(), mimetype=mimetype)
    filename = resume_book.name
    if request.GET.has_key('name'):
        filename = request.GET['name']
        resume_book.name = filename
    if request.GET['delivery_format'] == 'separate':
        response["Content-Disposition"] = 'attachment; filename="%s.zip"' % filename
    else:
        response["Content-Disposition"] = 'attachment; filename="%s.pdf"' % filename
    if redelivering:
        resume_book.last_updated = datetime.now()
    else:
        resume_book.delivered = True
    resume_book.save()
    return response


@user_passes_test(is_student)
@render_to("employer_snippets.html")
def employer_snippets(request, extra_context=None):
    if not request.user.student.profile_created:
        return redirect('student_profile')
    employers = employer_search_helper(request)
    subscriptions = request.user.student.subscriptions.all()
    for employer in employers:
        if employer in subscriptions:
            employer.subbed = True
    context = { 'employers': employers }
    context.update(extra_context or {})
    return context
    
    
@user_passes_test(is_student)
@render_to("employers.html")
def employers(request, extra_context=None):
    if not request.user.student.profile_created:
        return redirect('student_profile')
    
    subscriptions = request.user.student.subscriptions.all()

    employers = Employer.objects.filter(visible=True)
    for employer in employers:
        if employer in subscriptions:
            employer.subbed = True
            
    employer_id = int(request.GET.get('id', employers[0].id))
    try:
        employer = Employer.objects.get(id=employer_id)
    except Employer.DoesNotExist:
        return redirect('employers')
    
    subbed=False
    if employer in subscriptions:
        subbed = True

    context = {'industries':Industry.objects.all(),
               'employers':employers,
               'employer_id': employer_id,
               'employer': employer,
               'subbed': subbed }

    context.update(get_employer_upcoming_events_context(employer, request.user))
    context.update(extra_context or {})
    return context


@login_required
@user_passes_test(is_student)
@render_to('employer_details.html')
def employer_details(request, extra_content=None):
    if not request.GET.has_key("id"):
        raise Http400("Request is missing the employer id.")
    try:
        employer = Employer.objects.get(id=request.GET['id'])
    except:
        return Http404("Employer with id {0} not found".format(request.GET['id']))
    subscriptions = request.user.student.subscriptions.all()
    context = {
        'employer': employer,
        'subbed': employer in subscriptions
    }
    context.update(get_employer_upcoming_events_context(employer, request.user))
    return context


@login_required
@user_passes_test(is_student)
def employer_subscribe(request):
    if not request.POST.has_key("id"):
        raise Http400("Request is missing the id.")
    id = request.POST["id"]
    try:
        employer = Employer.objects.get(id=id)
    except Employer.DoesNotExist:
        raise Http404("Employer with id %s was not found." % id)
    if employer in request.user.student.subscriptions.all():
        request.user.student.subscriptions.remove(employer)
    else:
        request.user.student.subscriptions.add(employer) 
    # Update index
    employer.save()
    return HttpResponse()
