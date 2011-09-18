from __future__ import division
from __future__ import absolute_import

from datetime import datetime, timedelta
import operator

from django.conf import settings as s
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import URLValidator
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import simplejson
from django.views.decorators.http import require_GET

from core import enums, messages
from core.decorators import render_to, is_student, is_recruiter, is_campus_org, has_any_subscription, has_annual_subscription
from core.forms import BetaForm, AkismetContactForm
from core.models import Course, Language, Topic, Location, Question
from core.view_helpers import employer_campus_org_slug_exists
from campus_org.models import CampusOrg
from employer.forms import StudentSearchForm
from student.models import Student

from events.models import Event, FeaturedEvent
from haystack.query import SearchQuerySet, SQ
from notification.models import Notice
from registration.models import InterestedPerson

@require_GET
def check_employer_campus_org_slug_uniqueness(request):
    if request.is_ajax():
        if request.GET.has_key("slug"):
            data = False
            campusorg = None
            employer = None
            if is_campus_org(request.user):
                campusorg = request.user.campusorg
            elif is_recruiter(request.user):
                employer = request.user.recruiter.employer
            if not employer_campus_org_slug_exists(request.GET["slug"], campusorg=campusorg, employer=employer):
                data = True
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Request is missing the slug.")
    else:
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest")
    
@render_to('help_center.html')
def help_center(request, extra_context = None):
    questions = Question.objects.visible()
    if is_recruiter(request.user):
        questions = questions.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
    elif is_student(request.user):
        questions = questions.filter(Q(audience=enums.STUDENT) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
    elif is_campus_org(request.user):
        questions = questions.filter(Q(audience=enums.CAMPUS_ORG) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))            
    else:
        questions = questions.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
    context = {'top_questions':questions.order_by("-click_count")[:10]}
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
    if request.method == "POST":
        if request.POST.has_key("question_id"):
            q = Question.objects.get(id=request.POST["question_id"])
            q.click_count += 1
            q.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest("Question id is missing.")
    else:
        context = {'topics':[]}
        for topic in Topic.objects.all():
            questions = topic.question_set.visible()         
            if is_recruiter(request.user):
                questions = questions.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
            elif is_student(request.user):
                questions = questions.filter(Q(audience=enums.STUDENT) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
            elif is_campus_org(request.user):
                questions = questions.filter(Q(audience=enums.CAMPUS_ORG) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))            
            else:
                questions = questions.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
            if questions:
                context['topics'].append({'name': topic, 'questions':questions})
        context.update(extra_context or {})  
        return context

@render_to('about.html')
def about(request, extra_context = None):    
    context = {'campus_orgs':CampusOrg.objects.all(),
               'locations':Location.objects.all(),
               'courses':Course.objects.all()}
    context.update(extra_context or {})
    return context

@render_to('tutorials.html')
def tutorials(request, extra_context = None):
    context = {}
    context.update(extra_context or {})
    return context


@render_to('contact_us.html')
def contact_us(request, form_class = AkismetContactForm, fail_silently = False, extra_context=None):
    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST, request=request)
            if form.is_valid():
                form.save(fail_silently=fail_silently)
                data = {'valid':True}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                data = {'valid':False, 'errors':form.errors}
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
    else:
        return HttpResponseBadRequest("Request must be ajax.")

@login_required
@has_annual_subscription
def get_location_guess(request):
    if request.method == "GET":
        if request.GET.has_key('query'):
            sqs = SearchQuerySet().models(Location).filter(content=request.GET['query'])[:10]
            if not sqs or len(sqs) > 1:
                data = {'single':False, 'query':request.GET['query']}
            else:
                location = sqs[0].object
                data = {'single':True, 'latitude':location.latitude,
                        'longitude':location.longitude}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseBadRequest("Term for which to find suggestions is missing.")
    return HttpResponseForbidden("Request must be a GET")


@login_required
@has_annual_subscription
@render_to("location_suggestions.html")
def get_location_suggestions(request):
    if request.GET.has_key('query'):
        query = request.GET['query']
        suggestions = []
        if len(query.split("-")) > 1 and query.split("-")[1] and Location.objects.filter(building_num=query.split("-")[0]).exists():
            locations = Location.objects.filter(building_num__iexact=query.split("-")[0])[:8]
            for l in locations:
                suggestions.append({'name':"%s" % query, 'lat':l.latitude, 'lng':l.longitude})
        else:
            locations = SearchQuerySet().models(Location).filter(reduce(operator.__and__, [SQ(content_auto=word.strip()) for word in request.GET['query'].strip().split(' ')]))[:8]
            for l in locations:
                suggestions.append({'name':"%s" % str(l.object), 'lat':l.object.latitude, 'lng':l.object.longitude})
        context = {'suggestions': suggestions}
        return context
    else:
        return HttpResponseBadRequest("You must pass in either a query or an address to display.")

def landing_page_wrapper(request, extra_context=None):
    if request.user.is_authenticated():
        return home(request, extra_context=extra_context)
    else:
        return landing_page(request, extra_context=extra_context)

@render_to('landing_page.html')
def landing_page(request, extra_context = None):
    form_class = BetaForm
    
    posted = False
    disabled = False
    form_error = False
    email_error = False
    loggedout = False

    if request.GET.get('action', None) == 'logged-out':
        loggedout = True
    
    if request.method=="POST":
        form = form_class(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.ip_address = request.META['REMOTE_ADDR']
            person.save()
            
            subject = "[Umeqo] "+form.cleaned_data['email']+" signed up via landing page"
            message = "%s %s (%s) signed up!" % (form.cleaned_data['first_name'],form.cleaned_data['last_name'],form.cleaned_data['email'])
            sender = s.DEFAULT_FROM_EMAIL
            recipients = map(lambda n: n[1], s.ADMINS)
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
            'loggedout': loggedout,
            'form_error': form_error,
            'email_error': email_error,
    }
    if FeaturedEvent.objects.all().exists():
        context['featured_event'] = FeaturedEvent.objects.all().order_by("date_created")[0]
        
    if request.GET.has_key("action") and request.GET['action'] == "account-deactivated":
        context['deactivated'] = True
    context.update(extra_context or {})
    return context

@has_any_subscription
@render_to()
def home(request, extra_context=None):
    context = {}
    page_messages = { 'profile-saved': messages.profile_saved }
    msg = request.GET.get('msg',None)
    if msg:
        context.update(msg = page_messages[msg])
    if request.user.is_authenticated():
        if is_student(request.user):
            if not request.user.student.profile_created:
                return redirect('student_profile')
            private_events = Event.objects.filter(is_public=False).filter(invitee__student__in=[request.user.student]).distinct().filter(end_datetime__gt=datetime.now()).order_by('end_datetime')
            context['private_events'] = private_events
            subscriptions = request.user.student.subscriptions.all()
            if len(subscriptions) > 0:
                context['has_subscriptions'] = True
                sub_events = Event.objects.filter(is_public=True).filter(attending_employers__in=subscriptions).distinct().filter(end_datetime__gt=datetime.now()).order_by('end_datetime')
                context.update({
                    'has_subscriptions': True,
                    'sub_events':sub_events
                })
            else:
                context['has_subscriptions'] = False
            context.update(extra_context or {})
            context.update({'TEMPLATE':'student_home.html'})
            return context
        elif is_recruiter(request.user):
            now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
            your_events = Event.objects.filter(Q(owner=request.user) | Q(attending_employers__in=[request.user.recruiter.employer]))
            context.update({
                'search_form': StudentSearchForm(),
                'notices': Notice.objects.notices_for(request.user),
                'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                'upcoming_events': your_events.filter(Q(end_datetime__gte=now_datetime) | Q(type__name="Rolling Deadline")).order_by("end_datetime"),
                'past_events': your_events.filter(end_datetime__lt=now_datetime).order_by("-end_datetime"),
                'subscribers': Student.objects.filter(subscriptions__in=[request.user.recruiter.employer]).count()
            });
            context.update(extra_context or {})
            context.update({'TEMPLATE':'employer_home.html'})
            return context
        elif is_campus_org(request.user):
            now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:00')
            context.update({
                'notices': Notice.objects.notices_for(request.user),
                'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                'upcoming_events': Event.objects.filter(owner=request.user, end_datetime__gte=now_datetime).order_by("end_datetime"),
                'past_events': Event.objects.filter(owner=request.user, end_datetime__lt=now_datetime).order_by("-end_datetime")
            });
            context.update(extra_context or {})
            context.update({'TEMPLATE':'campus_org_home.html'})
            return context
    request.session.set_test_cookie()
    context.update({
        'login_form': AuthenticationForm,
        'action': request.REQUEST.get('action', ''),
        'TEMPLATE': 'anonymous_home.html'
    })
    event_kwargs = {}
    event_kwargs['end_datetime__gt'] = datetime.now()
    events = Event.objects.filter(**event_kwargs).order_by("end_datetime")
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
def check_language_uniqueness(request):
    
    if request.is_ajax():
        if Language.objects.filter(name=request.GET.get("name", "")).exists():
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        else:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")

@login_required
def get_notice_unseen_count(request):
    count = Notice.objects.unseen_count_for(request.user, on_site=True)
    return HttpResponse(simplejson.dumps({'count': count}), mimetype="application/json")

@render_to('500.html')
def handle_500(request, extra_context = None):
    context = {}
    if not request.user.is_authenticated():
        context = {'login_form': AuthenticationForm}
    context.update(extra_context or {})
    return context

@render_to('404.html')
def handle_404(request, extra_context = None):
    context = {}
    if not request.user.is_authenticated():
        context = {'login_form': AuthenticationForm}
    context.update(extra_context or {})
    return context

@render_to('403.html')
def handle_403(request, extra_context = None):
    context = {}
    if not request.user.is_authenticated():
        context = {'login_form': AuthenticationForm}
    context.update(extra_context or {})
    return context

@render_to('cache_status.html')
def cache_status(request, extra_context = None):
    try:
        import memcache
    except ImportError:
        raise Http404

    if not (request.user.is_authenticated() and request.user.is_staff):
        raise Http404
    
    cache_location = s.CACHES['default']['LOCATION']
    host = memcache._Host(cache_location)
    host.connect()
    host.send_cmd("stats")

    class Stats:
        pass

    stats = Stats()

    while True:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = timedelta(seconds=value)
            elif key == "time":
                value = datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()

    hit_rate = 100 * stats.get_hits / stats.cmd_get if stats.cmd_get else 'NaN'

    context = {
        'stats': stats,
        'hit_rate': '%.3f' % hit_rate,
        'time': datetime.now()
    }

    return context
