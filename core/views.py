"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import datetime

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from employer.forms import SearchForm
from notification.models import Notice
from core.models import Course, CampusOrg, Language, Topic
from core.view_helpers import does_email_exist
from registration.models import InterestedPerson
from core.forms import BetaForm, AkismetContactForm
from employer.models import Employer
from events.models import Event
from core import enums
from core import messages


def help(request,
         template_name='help.html',
         extra_context = None):
    
    context = {'topics':[]}
    if hasattr(request.user, "employer"):
        topics = Topic.objects.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.ALL))
    elif hasattr(request.user, "student"):
        topics = Topic.objects.filter(Q(audience=enums.STUDENT) | Q(audience=enums.ALL))
    else:
        topics = Topic.objects.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
        
    for topic in topics:
        questions = topic.question_set.filter(status = enums.ACTIVE)
        if hasattr(request.user, "employer"):
            questions = topic.question_set.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.ALL))
        elif hasattr(request.user, "student"):
            questions = topic.question_set.filter(Q(audience=enums.STUDENT) | Q(audience=enums.ALL))
        else:
            questions = topic.question_set.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
        
        context['topics'].append({'name': topic, 'questions':questions})

    context.update(extra_context or {})  
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

# Ajax-Only View
def contact_us_dialog(request,
                      template_name='contact_dialog.html',
                      form_class=AkismetContactForm,
                      fail_silently=False,
                      extra_context=None):

    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST, request=request)
            if form.is_valid():
                form.save(fail_silently=fail_silently)
                return HttpResponse(simplejson.dumps({"valid":True}))
            else:
                print form.errors
                print form.non_field_errors()
                data = {'valid':False}
                if form['body'].errors:
                    data['body_errors'] = str(form["body"].errors)
                if form.non_field_errors():
                    data['non_field_errors'] = str(form.non_field_errors())
                return HttpResponse(simplejson.dumps(data))
        else:
            form = form_class(request=request)
    
        context = {
                'form': form,
                'thank_you_for_contacting_us_message' : messages.thank_you_for_contacting_us
                }
        context.update(extra_context or {}) 
        return render_to_response(template_name,
                                  context,
                                  context_instance=RequestContext(request))
    return redirect('home')

def landing_page(request,
            template_name="landing_page.html",
            form_class = BetaForm,
            extra_context = None):
    
    posted = False
    disabled = False
    form_error = False
    email_error = False
    
    if request.method=="POST":
        form = form_class(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.ip_address = request.META['REMOTE_ADDR']
            person.save()
            
            subject = "[Umeqo] "+form.cleaned_data['email']+" signed up via landing page"
            message = "%s %s (%s) signed up!" % (form.cleaned_data['first_name'],form.cleaned_data['last_name'],form.cleaned_data['email'])
            sender = settings.DEFAULT_FROM_EMAIL
            recipients = map(lambda n: n[1],settings.ADMINS)
            send_mail(subject,message,sender,recipients)
            posted = True
            disabled = True
        else:
            if InterestedPerson.objects.filter(email=request.POST.get('email')).exists():
                email_error = True
            form_error = True
    else:
        form = form_class()
        
    context = {
            'form': form,
            'posted': posted,
            'disabled': disabled,
            'form_error': form_error,
            'email_error': email_error
    }

    context.update(extra_context or {})
    return render_to_response(template_name, context ,context_instance=RequestContext(request))


def home(request,
         anonymous_home_template_name="anonymous_home.html",
         student_home_template_name="student_home.html",
         employer_home_template_name="employer_home.html",
         extra_context=None):
    if request.user.is_authenticated():
        if hasattr(request.user, "student"):
            if not request.user.student.profile_created:
                return redirect('student_edit_profile')
            
            context = {}
            context.update(extra_context or {}) 
            return render_to_response(student_home_template_name,
                                      context,
                                      context_instance=RequestContext(request))
            
        elif hasattr(request.user, "employeruser"):
            
            your_events = request.user.employeruser.event_set.filter(end_datetime__gte=datetime.datetime.now()).order_by("start_datetime")
            
            context = {
                       'search_form': SearchForm(),
                       'notices': Notice.objects.notices_for(request.user),
                       'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                       'your_events': your_events
                       }
            
            context.update(extra_context or {})
            return render_to_response(employer_home_template_name, 
                                      context, 
                                      context_instance=RequestContext(request))
    
    request.session.set_test_cookie()
    
    context = {
               'login_form':AuthenticationForm,
               'action':request.REQUEST.get('action', '')
               }
    
    event_kwargs = {}
    event_kwargs['start_datetime__gt'] = datetime.datetime.now()
    events = Event.objects.filter(**event_kwargs).order_by("-start_datetime")
    context['events'] = list(events)[:3]
    
    context.update(extra_context or {})
    return render_to_response(anonymous_home_template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def check_website(request):
    
    if request.is_ajax():
        url_validator =  URLValidator(verify_exists = False)
        website = request.GET.get("website", "")
        try:
            url_validator(website)
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
        except ValidationError:
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return redirect('home')


def check_password(request):
    
    if request.is_ajax():
        if request.user.check_password(request.GET.get("password")):
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
        else:
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return redirect('home')


def check_username_existence(request):
    
    if request.is_ajax():
        username = request.GET.get("username", "")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                User.objects.get(email=username)
            except User.DoesNotExist:
                try:
                    Employer.objects.get(company_name = username)
                except Employer.DoesNotExist:
                    return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return redirect('home')
 
def check_email_existence(request):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps(does_email_exist(request.GET.get("email", ""))), mimetype="application/json")
    return redirect('home')


def check_email_availability(request):
    
    if request.is_ajax():
        try:
            User.objects.get(email=request.GET.get("email", ""))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except User.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return redirect('home')

@login_required
def check_event_name_uniqueness(request):

    if request.is_ajax():
        try:
            Event.objects.get(name=request.GET.get("name", ""))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except Event.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return redirect('home')

@login_required
def get_major_info(request,
                   template_name="major_info.html",
                   extra_context = None):
    
    if request.is_ajax():
        try:
            major = Course.objects.get(name=request.GET.get('course_name', ''))
            context = {'name': major.name,
                       'num': major.num, 
                       'admin' : major.admin,
                       'email': major.email,
                       'website':major.website,
                       'description': major.description,
                       'image':major.image.name}
            
            context.update(extra_context or {})
            return render_to_response(template_name,
                                      context,
                                      context_instance=RequestContext(request))
        except:
            return HttpResponseNotFound()
    return redirect('home')


@login_required
def check_campus_organization_uniqueness(request):
    
    if request.is_ajax():
        try:
            CampusOrg.objects.get(name=request.GET.get("name"))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except CampusOrg.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return redirect('home')


@login_required
def check_language_uniqueness(request):
    
    if request.is_ajax():
        try:
            Language.objects.get(name=request.GET.get("name", "") + " (Fluent)")
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except Language.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return redirect('home')


def browser_configuration_not_supported(request,
                                        template_name="browser_configuration_not_supported.html",
                                        extra_context=None):
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))
