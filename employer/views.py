from __future__ import division
from __future__ import absolute_import

import cStringIO
import mimetypes
import os
import re

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from pyPdf import PdfFileWriter, PdfFileReader
from datetime import datetime, date

from django.db.models import Q
from django.core.files import File
from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.http import require_POST, require_GET
from django.core.urlresolvers import reverse

from core.decorators import has_any_subscription, has_annual_subscription, is_student, is_student_or_recruiter, is_recruiter, render_to
from core.models import Industry
from registration.forms import PasswordChangeForm
from core import messages
from employer import enums as employer_enums
from employer.models import ResumeBook, Recruiter, Employer, EmployerStudentComment
from employer.forms import EmployerProfileForm, RecruiterForm, RecruiterPreferencesForm, StudentFilteringForm, StudentSearchForm, DeliverResumeBookForm
from employer.views_helper import get_paginator, employer_search_helper
from student import enums as student_enums
from subscription.models import EmployerSubscription, Subscription
from student.models import Student

@require_GET
@render_to("employer.html")
def employer(request):
    if request.GET.has_key("employer_name"):
        try:
            e = Employer.objects.get(name=request.GET['employer_name'])
            return {'employer': e}
        except:
            return HttpResponseNotFound("Employer with name %s does not exist" % (request.GET['name']))
    else:
        return HttpResponseBadRequest("Employer name is missing.")
    
@login_required
@user_passes_test(is_student_or_recruiter, login_url=s.LOGIN_URL)
@has_annual_subscription
@render_to("employer_profile_preview.html")
def employer_profile_preview(request, slug, extra_context=None):
    try:
        employer = Employer.objects.get(slug=slug)
    except Employer.DoesNotExist:
        raise Http404
    
    if is_student(request.user):
        return HttpResponseRedirect("%s?id=%s" % (reverse("employers_list"), employer.id))
    elif is_recruiter(request.user):
        context = {'employer':employer, 'upcoming_events':employer.event_set.filter(Q(end_datetime__gte=datetime.now().strftime('%Y-%m-%d %H:%M:00')) | Q(type__name="Rolling Deadline")).order_by("end_datetime"), 'preview':True}
        context.update(extra_context or {})
        return context
    
@login_required
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
@has_annual_subscription
@render_to("employer_recruiter_new.html")
def employer_recruiter_new(request, form_class=RecruiterForm, extra_context=None):
    if request.is_ajax():
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
    else:
        return HttpResponseBadRequest("Request must be ajax.")

@login_required
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
@render_to("employer_account.html")
@require_GET
def employer_account(request, preferences_form_class = RecruiterPreferencesForm, change_password_form_class = PasswordChangeForm, extra_context=None):
    context = {}
    msg = request.GET.get('msg', None)
    if msg:
        page_messages = {
            'password-changed': messages.password_changed,
        }
        context["msg"] = page_messages[msg]
    try:
        es = request.user.recruiter.employer.employersubscription
        free_trial = Subscription.objects.get(name="Free Trial")
        if es == free_trial:
            if not es.expired:
                context["subscription_button_text"] = "Upgrade Subscription"
        else:
            context["subscription_button_text"] = "Modify Subscription"
        context['subscription'] = es
        if es.cancelled:
            context['subscription_text'] = "Cancelled"
            context['subscription_class'] = "cancelled"
        elif es.expired():
            context['subscription_text'] = "Expired"
            context['subscription_class'] = "expired"
        else:
            if es.expires < date.today():
                context['subscription_text'] = "Grace Period"
                context['subscription_class'] = "grace"
            else:
                context['subscription_text'] = "Active"
                context['subscription_class'] = "active"
    except EmployerSubscription.DoesNotExist:
        context["subscription_button_text"] = "Subscribe"
    context['transactions'] = request.user.recruiter.employer.transaction_set.all().order_by("timestamp")
    context['other_recruiters'] = request.user.recruiter.employer.recruiter_set.exclude(id=request.user.recruiter.id)
    context['preferences_form'] = preferences_form_class(instance=request.user.recruiter.recruiterpreferences)
    context['change_password_form'] = change_password_form_class(request.user)
    context.update(extra_context or {})
    return context

@login_required
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
@render_to("employer_account_delete.html")
def employer_account_delete(request):

    if request.is_ajax():
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
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest") 

@login_required
@user_passes_test(is_recruiter)
@has_annual_subscription
@require_GET
@render_to("employer_other_recruiters.html")
def employer_other_recruiters(request):
    context = {'other_recruiters':request.user.recruiter.employer.recruiter_set.exclude(id=request.user.recruiter.id)}
    return context

@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_account_preferences(request, form_class=RecruiterPreferencesForm):
    form = form_class(data=request.POST, instance=request.user.recruiter.recruiterpreferences)
    data = []
    if form.is_valid():
        request.user.recruiter.recruiter_preferencess = form.save()
    else:
        data = {'errors': form.errors }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
@has_annual_subscription
@render_to("employer_profile.html")
def employer_profile(request, form_class=EmployerProfileForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.recruiter.employer)
        data = []
        if form.is_valid():
            form.save()
        else:
            data = {'errors': form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    else:
        context = {'form':form_class(instance=request.user.recruiter.employer),
                   'max_industries':s.EP_MAX_INDUSTRIES,
                   'edit':True}
        context.update(extra_context or {})
        return context
        
@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_student_toggle_star(request):
    if request.POST.has_key('student_id'):
        student = Student.objects.get(id=request.POST['student_id'])
        if student in request.user.recruiter.employer.starred_students.all():
            request.user.recruiter.employer.starred_students.remove(student)
            data = {'action':employer_enums.UNSTARRED}
        else:
            request.user.recruiter.employer.starred_students.add(student)
            data = {'action':employer_enums.STARRED}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        return HttpResponseBadRequest("Student ID is missing")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_students_add_star(request):
    if request.POST.has_key('student_ids'):
        for id in request.POST['student_ids'].split('~'):
            student = Student.objects.get(id=id)  
            if student not in request.user.recruiter.employer.starred_students.all():
                request.user.recruiter.employer.starred_students.add(student)
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Student IDs are missing")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_students_remove_star(request):
    if request.POST.has_key('student_ids'):
        for id in request.POST['student_ids'].split('~'):
            student = Student.objects.get(id=id)  
            if student in request.user.recruiter.employer.starred_students.all():
                request.user.recruiter.employer.starred_students.remove(student)
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Student IDs are missing")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_student_comment(request):
    if request.POST.has_key('student_id'):
        if request.POST.has_key('comment'):
            student = Student.objects.get(id=request.POST['student_id'])
            comment = request.POST['comment']
            try:
                student_comment = EmployerStudentComment.objects.get(student=student, employer=request.user.recruiter.employer)
            except EmployerStudentComment.DoesNotExist:
                EmployerStudentComment.objects.create(employer = request.user.recruiter.employer, student=student, comment=comment)
            student_comment.comment = comment
            student_comment.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest("Comment is missing.")
    else:
        return HttpResponseBadRequest("Student ID is missing.")

@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_resume_book_current_toggle_student(request):
    if request.POST.has_key('student_id'):
        student = Student.objects.get(id=request.POST['student_id'])
        try:
            resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
        except ResumeBook.DoesNotExist:
            resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
        if student in resume_book.students.all():
            resume_book.students.remove(student)
            data = {'action':employer_enums.REMOVED}  
        else:
            resume_book.students.add(student)
            student.studentstatistics.add_to_resumebook_count += 1
            student.studentstatistics.save()
            data = {'action':employer_enums.ADDED}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        return HttpResponseBadRequest("Student ID is missing.")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_resume_book_current_add_students(request):
    if request.POST.has_key('student_ids'):
        try:
            resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
        except ResumeBook.DoesNotExist:
            resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
        if request.POST['student_ids']:
            for id in request.POST['student_ids'].split('~'):
                student = Student.objects.get(id=id)
                if student not in resume_book.students.all():
                    resume_book.students.add(student)
                    student.studentstatistics.add_to_resumebook_count += 1
                    student.studentstatistics.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Student IDs are missing.")

@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_resume_book_current_remove_students(request):
    if request.POST.has_key('student_ids'):
        try:
            resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
        except ResumeBook.DoesNotExist:
            resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
        if request.POST['student_ids']:
            for student_id in request.POST['student_ids'].split('~'):
                student = Student.objects.get(id=student_id)  
                if student in resume_book.students.all():
                    resume_book.students.remove(student)
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Student IDs are missing.")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@render_to('employer_student_attendance.html')
def employer_student_event_attendance(request):
    if request.method == "GET":
        if request.GET.has_key('student_id'):
            context={}
            student = Student.objects.visible().get(id=request.GET['student_id'])
            context['events'] = request.user.event_set.filter(attendee__student=student)
            context['student'] = student
            return context
        else:
            return HttpResponseBadRequest("Student ID is missing.")
    else:
        return HttpResponseForbidden("Request must be a GET.")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_GET
@render_to("employer_resume_book_history.html")
def employer_resume_book_history(request, extra_context=None):
    context = {"resume_books":request.user.recruiter.resumebook_set.all(),
               'email_delivery_type': employer_enums.EMAIL}
    context.update(extra_context or {})
    return context


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@render_to()
def employer_students(request, extra_context=None):
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

        current_paginator = get_paginator(request)
        try:
            context['page'] = current_paginator.page(request.POST['page'])
        except Exception:
            context['page'] = current_paginator.page(1)
        context['current_student_list'] = request.POST['student_list']
        
        # I don't like this method of statistics
        for student, is_in_resume_book, is_starred, comment, num_of_events_attended in context['page'].object_list:
            student.studentstatistics.shown_in_results_count += 1
            student.studentstatistics.save()
        
        context['TEMPLATE'] = 'employer_students_results.html'
        context.update(extra_context or {}) 
        return context
    else:
        cache.delete('paginator')
        cache.delete('ordered_results')
        cache.delete('filtering_results')
        cache.delete('search_results')

        page_messages = {
            'NO_STUDENTS_SELECTED_MESSAGE': messages.no_students_selected,
            'WAIT_UNTIL_RESUME_BOOK_IS_READY_MESSAGE': messages.wait_until_resume_book_is_ready
        }
        context['page_messages'] = page_messages

        if request.method == "POST" and request.POST.has_key('query'):
            context['query'] = request.POST.get('query', '')
        
        # Passing the employer id to generate tha appropriate student list choices
        context['student_filtering_form'] = StudentFilteringForm(initial={
                'employer_id': request.user.recruiter.employer.id,
                'ordering': request.user.recruiter.recruiterpreferences.default_student_result_ordering,                           
                'results_per_page': request.user.recruiter.recruiterpreferences.default_student_results_per_page
        })
        context['student_search_form'] = StudentSearchForm()
        context['added'] = employer_enums.ADDED
        context['starred'] = employer_enums.STARRED
        context['email_delivery_type'] = employer_enums.EMAIL
        context['in_resume_book_student_list'] = student_enums.GENERAL_STUDENT_LISTS[2][1]
    context['TEMPLATE'] = 'employer_students.html'
    context.update(extra_context or {})
    return context


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@render_to('employer_resume_book_current_summary.html')
def employer_resume_book_current_summary(request, extra_context=None):
    try:
        resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = request.user.recruiter)
    context = {'resume_book': resume_book}
    context.update(extra_context or {}) 
    return context


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@render_to('employer_resume_book_current_deliver.html')
def employer_resume_book_current_deliver(request, form_class=DeliverResumeBookForm, extra_context=None):
    if request.is_ajax():
        context = {}
        if request.method == 'GET':
            context['deliver_resume_book_form'] = form_class(initial={'emails':request.user.email})
            if request.GET.has_key("resume_book_id"):
                if request.GET["resume_book_id"]:
                    try:
                        context['resume_book'] = ResumeBook.objects.get(id=request.GET["resume_book_id"])
                    except ResumeBook.DoesNotExist:
                        return HttpResponseBadRequest("No resume book exists with id of %s" % request.GET["resume_book_id"])
                else:
                    try:
                        context['resume_book'] = ResumeBook.objects.get(recruiter=request.user.recruiter, delivered=False)
                    except ResumeBook.DoesNotExist:
                        return HttpResponseBadRequest("There isn't a resume book ready to be delivered.")
                context.update(extra_context or {})
                return context
            else:
                return HttpResponseBadRequest("Request is missing a resume book id (it can be none).")   
        return HttpResponseBadRequest("Request must be a GET")       
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@require_POST
def employer_resume_book_current_create(request):
    
    if request.POST.has_key("resume_book_id") and request.POST['resume_book_id']:
        try:
            current_resume_book = ResumeBook.objects.get(id=request.POST["resume_book_id"])
        except ResumeBook.DoesNotExist:
            return HttpResponseBadRequest("No resume book exists with id of %s" % request.POST["resume_book_id"])
    else:
        try:
            current_resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
        except Exception:
            return HttpResponseBadRequest("There isn't a resume book ready to be made")
            
    report_buffer = cStringIO.StringIO() 
    c = Canvas(report_buffer)  
    c.drawString(1*cm, 28.5*cm, str(datetime.now().strftime('%m/%d/%Y') + " Resume Book"))
    c.drawString(1*cm, 28*cm, str(request.user.recruiter))
    c.drawString(1*cm, 27.5*cm, str(request.user.recruiter.employer))
    c.drawString(16*cm, 28.5*cm, "Created using Umeqo")
    for page_num, student in enumerate(current_resume_book.students.all()):
        c.drawString(4*cm, (25.5-page_num)*cm, student.first_name + " " + student.last_name)
        c.drawString(16*cm, (25.5-page_num)*cm, str(page_num+1))
    c.showPage()
    c.save()
    output = PdfFileWriter()
    output.addPage(PdfFileReader(cStringIO.StringIO(report_buffer.getvalue())) .getPage(0)) 
    for student in current_resume_book.students.all():
        output.addPage(PdfFileReader(file("%s%s" % (s.MEDIA_ROOT, str(student.resume)), "rb")).getPage(0))
    resume_book_name = "%s_%s" % (str(request.user), datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),)
    current_resume_book.resume_book_name = resume_book_name
    current_resume_book.save()
    file_path = "%semployer/resumebook/"% (s.MEDIA_ROOT,)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = "%s%s.tmp" % (file_path, resume_book_name,)
    outputStream = file(file_name, "wb")
    output.write(outputStream)
    outputStream.close()
    resume_book_contents = file(file_name, "rb")
    current_resume_book.resume_book.save(file_name, File(resume_book_contents))
    resume_book_contents.close()
    return HttpResponse()


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
@render_to("employer_resume_book_current_delivered.html")
def employer_resume_book_current_email(request, extra_context=None):
    if request.method == 'POST':
        if request.POST.has_key('emails'):
            if request.POST.has_key("resume_book_id") and request.POST['resume_book_id']:
                try:
                    current_resume_book = ResumeBook.objects.get(id=request.POST["resume_book_id"])
                except ResumeBook.DoesNotExist:
                    return HttpResponseBadRequest("No resume book exists with id of %s" % request.POST["resume_book_id"])
            else:
                try:
                    current_resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
                except Exception:
                    return HttpResponseBadRequest("There isn't a resume book ready to be made")
            reg = re.compile(r"\s*[;, \n]\s*")
            recipients = reg.split(request.POST['emails'])
            subject = ''.join(render_to_string('resume_book_email_subject.txt', {}).splitlines())
            body = render_to_string('resume_book_email_body.txt', {})
            message = EmailMessage(subject, body, s.DEFAULT_FROM_EMAIL, recipients)
            f = open("%s%s" % (s.MEDIA_ROOT, current_resume_book.resume_book.name), "rb")
            content = f.read()
            if request.POST.has_key('name') and request.POST['name']:
                filename = request.POST['name']
            else:
                filename = os.path.basename(current_resume_book.resume_book.name)
            message.attach("%s.pdf" % (filename), content, "application/pdf")
            message.send()
            current_resume_book.name = filename
            current_resume_book.delivered = True
            current_resume_book.save()
            context = {}
            context.update(extra_context or {})
            return context
        else:
            return HttpResponseBadRequest("Missing recipient email.")
    else:
        return HttpResponseBadRequest("Request must be a POST")


@login_required
@user_passes_test(is_recruiter)
@has_any_subscription
def employer_resume_book_current_download(request):
    if request.method == 'GET':
        if request.GET.has_key("resume_book_id") and request.GET['resume_book_id']:
            try:
                current_resume_book = ResumeBook.objects.get(id=request.GET["resume_book_id"])
            except ResumeBook.DoesNotExist:
                return HttpResponseBadRequest("No resume book exists with id of %s" % request.GET["resume_book_id"])
        else:
            try:
                current_resume_book = ResumeBook.objects.get(recruiter = request.user.recruiter, delivered=False)
            except Exception:
                return HttpResponseBadRequest("There isn't a resume book ready to be made")
        mimetype = mimetypes.guess_type(str(current_resume_book.resume_book))[0]
        if not mimetype: mimetype = "application/octet-stream"
        response = HttpResponse(file("%s%s" % (s.MEDIA_ROOT, current_resume_book.resume_book.name), "rb").read(), mimetype=mimetype)
        filename = os.path.basename(current_resume_book.resume_book.name)
        if request.GET.has_key('name'):
            filename = request.GET['name']
        response["Content-Disposition"]= 'attachment; filename="%s"' % filename
        current_resume_book.name = filename
        current_resume_book.delivered = True
        current_resume_book.save()
        return response
    else:
        return HttpResponseBadRequest("Request must be a GET")


@login_required
@user_passes_test(is_student)
@render_to('employers_list.html')
def employers_list(request, extra_content=None):
    if not request.user.student.profile_created:
        return redirect('student_profile')
    
    query = request.GET.get('q', '')
    employers = employer_search_helper(request)
    industries = Industry.objects.all()
    subscriptions = request.user.student.subscriptions.all()
    sub_status = {}
    for employer in employers:
        if employer in subscriptions:
            employer.subscribed = True
        else:
            employer.subscribed = False
    context = {
        'employers': employers,
        'industries': industries,
        'query': query,
        'sub_status': sub_status
    }
    if len(employers) > 0:
        employer_id = request.GET.get('id', None)
        if employer_id:
            try:
                employer_id = int(employer_id)
                employer = Employer.objects.get(id=employer_id)
            except (ValueError, ObjectDoesNotExist):
                return redirect('employers_list')
        else:
            employer = employers[0]
            employer_id = employer.id

        subbed = employer in subscriptions
        
        context.update({
            'employer': employer,
            'upcoming_events': employer.event_set.filter(Q(end_datetime__gte=datetime.now().strftime('%Y-%m-%d %H:%M:00')) | Q(type__name="Rolling Deadline")),
            'employer_id': employer_id,
            'subbed': subbed
        })
    return context


@login_required
@user_passes_test(is_student)
@render_to('employers_list_pane.html')
def employers_list_pane(request, extra_content=None):
    employer_id = request.GET.get('id',None)
    if employer_id and Employer.objects.filter(id=employer_id).exists():
        employer = Employer.objects.get(id=employer_id)
        
        subscriptions = request.user.student.subscriptions.all()
        subbed = employer in subscriptions
        context = {
            'employer': employer,
            'upcoming_events': employer.event_set.filter(Q(end_datetime__gte=datetime.now().strftime('%Y-%m-%d %H:%M:00')) | Q(type__name="Rolling Deadline")),
            'subbed': subbed
        }
        return context
    return HttpResponseBadRequest("Bad request. Employer id is missing.")


@login_required
@user_passes_test(is_student)
@render_to('employers_list_ajax.html')
def employer_list_ajax(request):
    employers = employer_search_helper(request)
    context = {'employers': employers}
    return context


@login_required
@user_passes_test(is_student)
def employer_subscribe(request):
    employer_id = request.POST.get('id', None)
    if employer_id and Employer.objects.filter(id=employer_id).exists():
        employer = Employer.objects.get(id=employer_id)
        student = request.user.student
        subscribe = request.POST.get('subscribe', None)
        if not subscribe:
            return HttpResponseBadRequest("Bad request.")
        subscribe = bool(int(subscribe))
        if subscribe:
            student.subscriptions.add(employer)
        elif employer in student.subscriptions.all() and not subscribe:
            student.subscriptions.remove(employer)
        else:
            return HttpResponseBadRequest("Bad request.")
        student.save()
        # Force save employer to have Haystack update index
        employer.save()
        data = {'valid':True,'subscribe':subscribe}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    return HttpResponseBadRequest("Bad request.")
