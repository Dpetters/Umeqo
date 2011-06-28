"""
 Developers : Dmitrij Petters, Joshua Ma
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
import mimetypes, os
import cStringIO

from datetime import datetime
from pyPdf import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas  
from reportlab.lib.units import cm
 
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import simplejson
from django.template.loader import render_to_string

from core.decorators import is_student, is_recruiter
from employer.models import ResumeBook, Employer, StudentComment
from employer.forms import DeliverResumeBookForm, EmployerPreferences, SearchForm, FilteringForm, StudentFilteringForm
from employer.view_helpers import get_paginator
from employer import enums as employer_enums
from events.forms import EventForm
from events.models import Event
from student.models import Student
from student import enums as student_enums
from operator import attrgetter

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
def employer_employer_profile(request, 
                             employer, 
                             template_name="employer_employer_profile.html", 
                             extra_context = None):
    if employer == str(request.user.recruiter.employer):
        context = {}
        context.update(extra_context or {})
        return render_to_response(template_name, 
                                  context, 
                                  context_instance=RequestContext(request))
    else:
        return redirect(reverse('employer_employer_profile', kwargs={'employer': request.user.recruiter.employer}))

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
def employer_students_comment(request,
                                        extra_context=None):
    
    if request.is_ajax():
        if request.POST.has_key('student_id'):
            if request.POST.has_key('comment'):
                student = Student.objects.get(id=request.POST['student_id'])
                comment = request.POST['comment']
                student_comments = StudentComment.objects.filter(student=student, recruiter=request.user.recruiter)
                if not student_comments.exists():
                    StudentComment.objects.create(recruiter = request.user.recruiter, student=student, comment=comment)
                else:
                    student_comment = student_comments[0]
                    student_comment.comment = comment
                    student_comment.save()
                data = {'valid':True}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                return HttpResponseBadRequest("Comment is missing")
        else:
            return HttpResponseBadRequest("Student ID is missing")
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
            if request.POST['student_ids']:
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
            if request.POST['student_ids']:
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
def employer_students(request,
                       result_template_name='employer_students_results.html',
                       filtering_page_template_name='employer_students.html',
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

        current_paginator = get_paginator(request)
        context['page'] = current_paginator.page(request.POST['page'])
        
        context['current_student_list'] = request.POST['student_list']
        
        for student, is_in_resume_book, is_starred, comment in context['page'].object_list:
            student.statistics.shown_in_results_count += 1
            student.save()
        
        context.update(extra_context or {}) 
        return render_to_response(result_template_name,
                                  context,
                                  context_instance=RequestContext(request))
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
        context['email_delivery_type'] = employer_enums.EMAIL
        context['in_resume_book_student_list'] = student_enums.GENERAL_STUDENT_LISTS[2][1]
        
    context.update(extra_context or {})
    return render_to_response(filtering_page_template_name, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_books_create(request):
    if request.is_ajax():
        if request.method == 'POST':
            latest_resume_book = ResumeBook.objects.filter(recruiter = request.user.recruiter).order_by('-date_created')[0]
            output = PdfFileWriter()
            report_buffer = cStringIO.StringIO() 
            c = canvas.Canvas(report_buffer)  
            c.drawString(8*cm, 26*cm, str(datetime.now().strftime('%m/%d/%Y') + " Resume Book"))
            c.drawString(9*cm, 25.5*cm, str(request.user.recruiter))
            c.drawString(8.5*cm, 25*cm, str(request.user.recruiter.employer))
            c.drawString(16*cm, 29*cm, "Created using Umeqo")
            page_num = 0
            for student in latest_resume_book.students.all():
                page_num += 1
                c.drawString(4*cm, (22-page_num)*cm, student.first_name + " " + student.last_name)
                c.drawString(16*cm, (22-page_num)*cm, str(page_num))
            c.showPage()
            c.save()
            pdfInput = PdfFileReader(cStringIO.StringIO(report_buffer.getvalue())) 
            output.addPage(pdfInput.getPage(0)) 
            for student in latest_resume_book.students.all():
                output.addPage(PdfFileReader(file(str(settings.MEDIA_ROOT).replace("\\", "/") + "/" + str(student.resume), "rb")).getPage(0))
            resume_book_name = str(request.user) + "_" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf";
            latest_resume_book.resume_book_name = resume_book_name
            if not os.path.exists(str(settings.RESUME_BOOK_ROOT)):
                os.mkdir(str(settings.RESUME_BOOK_ROOT))  
            outputStream = file(str(settings.RESUME_BOOK_ROOT) + resume_book_name, "wb")
            output.write(outputStream)
            latest_resume_book.file_name = resume_book_name
            latest_resume_book.save()
            data = {'valid':True}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        return HttpResponseBadRequest("Request must be a POST")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_books_email(request,
                                subject_template="resume_book_email_subject.txt",
                                body_template="resume_book_email_body.txt",
                                extra_context=None):
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST.has_key('email'):
                latest_resume_book = ResumeBook.objects.filter(recruiter = request.user.recruiter).order_by('-date_created')[0]
                recipients = [request.POST['email']]
                subject = ''.join(render_to_string(subject_template, {}).splitlines())
                body = render_to_string(body_template, {})
                message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
                message.attach_file(str(settings.RESUME_BOOK_ROOT) + str(latest_resume_book.file_name))
                message.send()
                os.remove(str(settings.RESUME_BOOK_ROOT) + str(latest_resume_book.file_name))
                data = {'valid':True}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                return HttpResponseBadRequest("Missing recipient email.")
        else:
            return HttpResponseBadRequest("Request must be a POST")
    HttpResponseForbidden("Request must be a valid XMLHttpRequest")
    
@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_books_download(request):
    if request.method == 'GET':
        latest_resume_book = ResumeBook.objects.filter(recruiter = request.user.recruiter).order_by('-date_created')[0]
        mimetype = mimetypes.guess_type(latest_resume_book.file_name)[0]
        if not mimetype: mimetype = "application/octet-stream"
        response = HttpResponse(file(str(settings.RESUME_BOOK_ROOT) + str(latest_resume_book.file_name), "rb").read(), mimetype=mimetype)
        filename = str(latest_resume_book.file_name)
        if request.GET.has_key('name'):
            filename = request.GET['name']
        response["Content-Disposition"]= "attachment; filename=%s" % filename
        os.remove(str(settings.RESUME_BOOK_ROOT) + str(latest_resume_book.file_name))
        return response
    else:
        return HttpResponseBadRequest("Request must be a GET")
    
@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_resume_books_deliver(request,
                                  form_class = DeliverResumeBookForm,
                                  template_name="employer_resume_books_deliver.html",
                                  extra_context=None):
    if request.is_ajax():
        context = {}
        if request.method == 'GET':
            context['deliver_resume_book_form'] = form_class(initial={'email':request.user.email})
            context['resume_book'] = ResumeBook.objects.filter(recruiter = request.user.recruiter).order_by('-date_created')[0]
            context.update(extra_context or {})
            return render_to_response(template_name,
                                      context,
                                      context_instance=RequestContext(request))
        return HttpResponseBadRequest("Request must be a GET")       
    HttpResponseForbidden("Request must be a valid XMLHttpRequest")

    
@login_required
@user_passes_test(is_recruiter, login_url=settings.LOGIN_URL)
def employer_invitations(request, template_name='employer_invitations.html', extra_context=None):
    context = {}
    context.update(extra_context or {})  
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def employers_list(request, template_name='employers_list.html', extra_content=None):
    employers = Employer.objects.all()
    try:
        employer_id = int(request.GET.get('id',None))
    except TypeError:
        employer = employers[0]
        employer_id = employer.id
    else:
        employer = employers.get(id=employer_id)
    recruiter = employer.recruiter_set.all()[0]
    
    now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
    events = reduce(
        lambda a,b: [a.extend(b.event_set.all().extra(select={'upcoming': 'end_datetime > "%s"' % now_datetime})),a][1],
        employer.recruiter_set.all(),
        []
    )
    context = {
        'employers': employers,
        'employer': employer,
        'events': events,
        'employer_id': employer_id
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def employers_list_el(request, template_name='employers_list_el.html', extra_content=None):
    employer_id = request.GET.get('id',None)
    if employer_id and Employer.objects.filter(id=employer_id).exists():
        employer = Employer.objects.get(id=employer_id)
        
        now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        events = reduce(
            lambda a,b: [a.extend(b.event_set.all().extra(select={'upcoming': 'end_datetime > "%s"' % now_datetime})),a][1],
            employer.recruiter_set.all(),
            []
        )
        events = sorted(events, key=attrgetter('end_datetime'), reverse=True)

        context = {
            'employer': employer,
            'events': events
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
        return HttpResponseBadRequest("Bad request.")
