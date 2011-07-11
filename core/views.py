from datetime import datetime

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden
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

from notification.models import Notice
from registration.models import InterestedPerson
from core import enums, messages
from core.decorators import render_to
from core.models import Course, CampusOrg, Language, Topic
from core.forms import BetaForm, AkismetContactForm
from core.view_helpers import does_email_exist
from employer.forms import SearchForm
from employer.models import Employer, Recruiter
from events.models import Event

@render_to('help_center.html')
def help_center(request, extra_context = None):
    
    context = {}
    context.update(extra_context or {})
    return context

def deactivate_account(request, extra_context = None):
    
    context = {}
    if hasattr(request.user, "student"):
        context['TEMPLATE'] = "student_deactivate_account.html"
    elif hasattr(request.user, "employer"):
        context['TEMPLATE'] = "student_deactivate_account.html"        
    context.update(extra_context or {})
    return context

@render_to('faq.html')
def faq(request, extra_context = None):
    
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
    return context

@render_to('tutorials.html')
def tutorials(request, extra_context = None):
    
    context = {}
    context.update(extra_context or {})
    return context

def contact_us_dialog(request, extra_context=None):

    form_class = AkismetContactForm
    fail_silently = False;

    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST, request=request)
            if form.is_valid():
                form.save(fail_silently=fail_silently)
                return HttpResponse(simplejson.dumps({"valid":True}), mimetype="application/json")
            else:
                data = {'valid':False}
                if form['body'].errors:
                    data['body_errors'] = str(form["body"].errors)
                if form.non_field_errors():
                    data['non_field_errors'] = str(form.non_field_errors())
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
        return render_to_response('contact_us_dialog.html',
                                  context,
                                  context_instance=RequestContext(request))
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


def home(request, extra_context=None):
    
    context = {}

    page_messages = {
        'profile_saved': messages.profile_saved
    }
    msg = request.GET.get('msg',None)
    if msg:
        context.update(msg = page_messages[msg])

    if request.user.is_authenticated():
        if hasattr(request.user, "student"):
            if not request.user.student.profile_created:
                return redirect('student_edit_profile')

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
            return render_to_response('student_home.html', context,
                    context_instance=RequestContext(request))
            
        elif hasattr(request.user, "recruiter"):
            
            now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
            your_events = request.user.recruiter.event_set.order_by("-end_datetime").extra(select={'upcoming': 'end_datetime > "%s"' % now_datetime})
            
            context.update({
                'teststring': 'asdlfkjasldfja sakfasdlfk asdl ashdfa sdlfja sdlf asdlf asldkjf askldf asjdfa sdfasdf',
                'search_form': SearchForm(),
                'notices': Notice.objects.notices_for(request.user),
                'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                'your_events': your_events
            });
            
            context.update(extra_context or {})
            return render_to_response('employer_home.html', context, 
                    context_instance=RequestContext(request))
    
    request.session.set_test_cookie()
    
    context.update({
        'login_form': AuthenticationForm,
        'action': request.REQUEST.get('action', '')
    })

    event_kwargs = {}
    event_kwargs['end_datetime__gt'] = datetime.now()
    events = Event.objects.filter(**event_kwargs).order_by("-end_datetime")
    context['events'] = list(events)[:3]
    
    context.update(extra_context or {})
    return render_to_response('anonymous_home.html', context,
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
def get_course_info(request, extra_context = None):

    if request.is_ajax():
        if request.GET.has_key('course_id'):
            courses = Course.objects.filter(id = request.GET['course_id'])
            if courses.exists():
                course = courses[0]
                context = {'name': course.name,
                           'num': course.num, 
                           'admin' : course.admin,
                           'email': course.email,
                           'website':course.website,
                           'description': course.description,
                           'image': course.image.name}
                context.update(extra_context or {})
                return render_to_response('course_info.html',
                                          context,
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseServerError("Course ID doesn't match any existing course's ID.")        
        else:
            return HttpResponseBadRequest("Course ID is missing.")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest.")

@login_required
def get_campus_org_info(request, extra_context = None):

    if request.is_ajax():
        if request.GET.has_key('campus_org_id'):
            campus_orgs = CampusOrg.objects.filter(id=request.GET['campus_org_id'])
            if campus_orgs.exists():
                campus_org = campus_orgs[0]
                context = {'name': campus_org.name,
                           'email': campus_org.email,
                           'website':campus_org.website,
                           'description': campus_org.description,
                           'image': campus_org.image.name}
                context.update(extra_context or {})
                return render_to_response('campus_org_info.html', context,
                        context_instance=RequestContext(request))
            else:
                return HttpResponseServerError("Campus Org ID doesn't match any existing campus org's ID.")        
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


@render_to('browser_configuration_not_supported.html')
def browser_configuration_not_supported(request, extra_context=None):
    context = {}
    context.update(extra_context or {})
    return context

def get_notice_unseen_count(request):
    count = Notice.objects.unseen_count_for(request.user, on_site=True)
    return HttpResponse(simplejson.dumps({'count': count}), mimetype="application/json")
