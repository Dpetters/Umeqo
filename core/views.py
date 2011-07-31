from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from haystack.query import SearchQuerySet
from notification.models import Notice
from registration.models import InterestedPerson
from core import enums, messages
from core.decorators import render_to
from core.models import Course, CampusOrg, Language, Topic, Location
from core.forms import BetaForm, AkismetContactForm
from core.view_helpers import does_email_exist
from employer.forms import StudentSearchForm
from employer.models import Employer, Recruiter
from events.models import Event

@render_to('help_center.html')
def help_center(request, extra_context = None):
    
    context = {}
    context.update(extra_context or {})
    return context

def account_deactivate(request, extra_context = None):
    
    context = {}
    if hasattr(request.user, "student"):
        context['TEMPLATE'] = "student_account_deactivate.html"
    elif hasattr(request.user, "employer"):
        context['TEMPLATE'] = "student_account_deactivate.html"        
    context.update(extra_context or {})
    return context


@render_to('faq.html')
def faq(request, extra_context = None):
    
    context = {'topics':[]}
    
    for topic in Topic.objects.all():
        questions = topic.question_set.filter(display = True)           
        if hasattr(request.user, "employer"):
            questions = topic.question_set.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
        elif hasattr(request.user, "student"):
            questions = topic.question_set.filter(Q(audience=enums.STUDENT) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
        elif hasattr(request.user, "campus_org"):
            questions = topic.question_set.filter(Q(audience=enums.CAMPUS_ORG) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))            
        else:
            questions = topic.question_set.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
        if questions:
            context['topics'].append({'name': topic, 'questions':questions})

    context.update(extra_context or {})  
    return context

@render_to('tutorials.html')
def tutorials(request, extra_context = None):
    
    context = {}
    context.update(extra_context or {})
    return context


@render_to('contact_us_dialog.html')
def contact_us_dialog(request, form_class = AkismetContactForm, fail_silently = False, extra_context=None):
    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST, request=request)
            if form.is_valid():
                form.save(fail_silently=fail_silently)
                return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
            else:
                data = {'valid':False}
                errors = {}
                for field in form:
                    if field.errors:
                        errors[field.auto_id] = field.errors[0]
                if form.non_field_errors():
                    errors['non_field_error'] = form.non_field_errors()[0]
                data['errors'] = errors
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            if request.user.is_authenticated():
                form = form_class(request=request, initial={'name': "%s %s" % (request.user.first_name, request.user.last_name,), 'email':request.user.email})
            else:
                form = form_class(request=request)                
        context = {
                'form': form,
                'thank_you_for_contacting_us_message' : messages.thank_you_for_contacting_us
                }
        context.update(extra_context or {}) 
        return context
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
def get_location_guess(request):
    if request.is_ajax():
        if request.method == "GET":
            if request.GET.has_key('query'):
                search_query_set = SearchQuerySet().models(Location).filter(content=request.GET['query'])[:10]
                if not search_query_set:
                    data = {'valid':False}
                    data['query'] = request.GET['query']
                else:
                    location = search_query_set[0].object
                    data = {'valid':True,
                            'latitude':location.latitude,
                            'longitude':location.longitude}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                return HttpResponseBadRequest("Term got which to find suggestions is missing.")
        return HttpResponseForbidden("Request must be a GET")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@render_to('landing_page.html')
def landing_page(request, extra_context = None):
    
    form_class = BetaForm

    if request.GET.get('magic','')!='' or request.user.is_authenticated():
        return home(request)
    
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
    return context

@render_to()
def home(request, extra_context=None):
    context = {}
    page_messages = { 'profile-saved': messages.profile_saved }
    msg = request.GET.get('msg',None)
    if msg:
        context.update(msg = page_messages[msg])
        
    if request.user.is_authenticated():
        if hasattr(request.user, "student"):
            if not request.user.student.profile_created:
                return redirect('student_profile')

            subscriptions = request.user.student.subscriptions.all()
            if len(subscriptions) > 0:
                context['has_subscriptions'] = True
                recruiters = Recruiter.objects.filter(employer__in=subscriptions)
                sub_events = Event.objects.filter(recruiters__in=recruiters).filter(end_datetime__gt=datetime.now())
                sub_events = sub_events.order_by('end_datetime')
                context.update({
                    'has_subscriptions': True,
                    'sub_events': sub_events
                })
            else:
                context['has_subscriptions'] = False
            context.update(extra_context or {}) 
            context.update({'TEMPLATE':'student_home.html'})
            return context
        elif hasattr(request.user, "recruiter"):
            now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
            your_events = request.user.recruiter.event_set.order_by("-end_datetime").extra(select={'upcoming': 'end_datetime > "%s"' % now_datetime})
            context.update({
                'search_form': StudentSearchForm(),
                'notices': Notice.objects.notices_for(request.user),
                'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                'your_events': your_events
            });
            context.update(extra_context or {})
            context.update({'TEMPLATE':'employer_home.html'})
            return context
    request.session.set_test_cookie()
    context.update({
        'login_form': AuthenticationForm,
        'action': request.REQUEST.get('action', ''),
        'TEMPLATE': 'anonymous_home.html'
    })
    event_kwargs = {}
    event_kwargs['end_datetime__gt'] = datetime.now()
    events = Event.objects.filter(**event_kwargs).order_by("-end_datetime")
    context['events'] = list(events)[:3]
    context.update(extra_context or {})
    return context


def check_website(request):
    if request.is_ajax():
        url_validator =  URLValidator(verify_exists = False)
        website = request.GET.get("website", "")
        try:
            url_validator(website)
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
        except ValidationError:
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


def check_password(request):
    if request.is_ajax():
        if request.user.check_password(request.GET.get("password")):
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
        else:
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


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
                    Employer.objects.get(name = username)
                except Employer.DoesNotExist:
                    return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

 
def check_email_existence(request):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps(does_email_exist(request.GET.get("email", ""))), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


def check_email_availability(request):
    if request.is_ajax():
        try:
            User.objects.get(email=request.GET.get("email", ""))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except User.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
def check_event_name_uniqueness(request):
    if request.is_ajax():
        try:
            Event.objects.get(name=request.GET.get("name", ""))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except Event.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
@render_to('course_info.html')
def course_info(request, extra_context = None):
    if request.is_ajax():
        if request.GET.has_key('course_id'):
            try:
                context = {}
                context['course'] = Course.objects.get(id = request.GET['course_id'])
                context.update(extra_context or {})
                return context
            except Course.DoesNotExist:
                return HttpResponseBadRequest("Course ID doesn't match any existing campus org's ID.")        
        else:
            return HttpResponseBadRequest("Course ID is missing.")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest.")


@login_required
@render_to('campus_org_info.html')
def campus_org_info(request, extra_context = None):
    if request.is_ajax():
        if request.GET.has_key('campus_org_id'):
            try:
                context = {}
                context['campus_org'] = CampusOrg.objects.get(id=request.GET['campus_org_id'])
                context.update(extra_context or {})
                return context
            except CampusOrg.DoesNotExist:
                return HttpResponseBadRequest("Campus Org ID doesn't match any existing campus org's ID.")        
        else:
            return HttpResponseBadRequest("Campus Org ID is missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
def check_campus_organization_uniqueness(request):
    if request.is_ajax():
        try:
            CampusOrg.objects.get(name=request.GET.get("name"))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except CampusOrg.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
def check_language_uniqueness(request):
    
    if request.is_ajax():
        try:
            Language.objects.get(name=request.GET.get("name", "") + " (Fluent)")
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except Language.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@render_to('unsupported_browser.html')
def unsupported_browser(request, extra_context=None):
    context = {}
    context.update(extra_context or {})
    return context

@login_required
def get_notice_unseen_count(request):
    count = Notice.objects.unseen_count_for(request.user, on_site=True)
    return HttpResponse(simplejson.dumps({'count': count}), mimetype="application/json")
