from __future__ import division
from __future__ import absolute_import

from datetime import datetime, timedelta
import operator

from django.conf import settings as s
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext, loader
from django.utils import simplejson
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET, require_http_methods

from campus_org.models import CampusOrg
from core import messages, enums as core_enums
from core.decorators import render_to, is_student, is_recruiter, is_campus_org, has_any_subscription, has_annual_subscription
from core.forms import AkismetContactForm
from core.http import Http403, Http400
from core.models import Course, Language, Location, Question, Topic, Tutorial
from core.view_helpers import employer_campus_org_slug_exists, filter_faq_questions
from employer.forms import StudentSearchForm
from employer.models import Employer
from events.models import Event, FeaturedEvent
from events.view_helpers import get_upcoming_events_context, get_upcoming_events_sqs, get_categorized_events_context
from haystack.query import SearchQuerySet, SQ
from notification.models import Notice
from student.forms import StudentRegistrationForm
from student.models import Student


@require_GET
@render_to('about.html')
def about(request, extra_context=None):
    context = {'campus_orgs':CampusOrg.objects.all(),
               'courses':Course.objects.all(),
               'employers':Employer.objects.all(),
               'languages':Language.objects.all(),
               'locations':Location.objects.all()}
    context.update(extra_context or {})
    return context


@require_GET
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

    context = {
        'stats': stats,
        'time': datetime.now()
    }
    if stats.cmd_get:
        context['hit_rate'] = 100 * stats.get_hits / stats.cmd_get
    return context


@require_GET
def check_employer_campus_org_slug_uniqueness(request):
    if not request.GET.has_key("slug"):
        raise Http400("Request GET is missing the slug.")
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

    
@require_GET
def check_employer_uniqueness(request):
    if not request.GET.has_key("name"):
        raise Http400("Request is missing the name.")
    try:
        Employer.objects.get(name=request.GET['name'])
        data = False
    except Employer.DoesNotExist:
        data = True
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@require_http_methods(["POST", "GET"])
@render_to('contact_us_dialog.html')
def contact_us(request, form_class = AkismetContactForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, request=request)
        if form.is_valid():
            form.save()
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
    context = { 'form': form,
                'thank_you_for_contacting_us_message' : messages.thank_you_for_contacting_us}
    context.update(extra_context or {}) 
    return context


@require_GET
@login_required
@has_annual_subscription
def get_location_guess(request):
    if not request.has_key("query"):
        raise Http400("Request GET is missing the query.") 
    sqs = SearchQuerySet().models(Location)
    sqs = search(sqs, request.GET.get('query', ""))[:10]
    if not sqs or len(sqs) > 1:
        data = {'single':False, 'query':request.GET['query']}
    else:
        loc = sqs[0].object
        data = {'single':True, 'latitude':loc.latitude, 'longitude':loc.longitude}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@require_GET
@login_required
@has_annual_subscription
@render_to("location_suggestions.html")
def get_location_suggestions(request):
    if not request.GET.has_key('query'):
        raise Http403("Request GET is missing the query.")
    num_of_suggestions = 7
    query = request.GET['query']
    suggestions = []
    if len(query.split("-")) > 1 and query.split("-")[1] and Location.objects.filter(building_num=query.split("-")[0]).exists():
        locations = Location.objects.filter(building_num__iexact=query.split("-")[0])[:num_of_suggestions]
        for l in locations:
            suggestions.append({'name':"%s" % query, 'lat':l.latitude, 'lng':l.longitude})
    else:
        locations = SearchQuerySet().models(Location).filter(reduce(operator.__and__, [SQ(text=word.strip()) for word in request.GET['query'].strip().split(' ')]))[:num_of_suggestions]
        for l in locations:
            suggestions.append({'name':"%s" % str(l.object), 'lat':l.object.latitude, 'lng':l.object.longitude})
    context = {'suggestions': suggestions}
    return context


@render_to('help_center.html')
@require_GET
def help_center(request, extra_context = None):
    context = {}
    tutorials = Tutorial.objects.filter(display=True)
    if request.user.is_anonymous or request.user.is_recruiter:
        recruiter_audience = [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_EMPLOYERS, core_enums.EMPLOYER, core_enums.CAMPUS_ORGS_AND_EMPLOYERS]
        try:
            context['recruiter_student_discovery_tutorials'] = tutorials.filter(audience__in = recruiter_audience, topic=Topic.objects.get(name="Student Discovery")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['recruiter_subscription_tutorials'] = tutorials.filter(audience__in = recruiter_audience, topic=Topic.objects.get(name="Subscriptions")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['recruiter_event_and_deadline_tutorials'] = tutorials.filter(audience__in = recruiter_audience, topic=Topic.objects.get(name="Events & Deadlines")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['recruiter_account_management_tutorials'] = tutorials.filter(audience__in = recruiter_audience, topic=Topic.objects.get(name="Account Management")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
    if request.user.is_anonymous or request.user.is_student:
        student_audience = [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_STUDENTS, core_enums.STUDENT]
        try:
            context['student_student_discovery_tutorials'] = tutorials.filter(audience__in = student_audience, topic=Topic.objects.get(name="Student Discovery")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['student_subscription_tutorials'] = tutorials.filter(audience__in = student_audience, topic=Topic.objects.get(name="Subscriptions")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['student_event_and_deadline_tutorials'] = tutorials.filter(audience__in = student_audience, topic=Topic.objects.get(name="Events & Deadlines")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['student_account_management_tutorials'] = tutorials.filter(audience__in = student_audience, topic=Topic.objects.get(name="Account Management")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
    if request.user.is_anonymous or request.user.is_campus_org:
        campus_org_audience = [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_CAMPUS_ORGS, core_enums.CAMPUS_ORG, core_enums.CAMPUS_ORGS_AND_EMPLOYERS]
        try:
            context['campus_org_student_discovery_tutorials'] = tutorials.filter(audience__in = campus_org_audience, topic=Topic.objects.get(name="Student Discovery")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['campus_org_subscription_tutorials'] = tutorials.filter(audience__in = campus_org_audience, topic=Topic.objects.get(name="Subscriptions")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['campus_org_event_and_deadline_tutorials'] = tutorials.filter(audience__in = campus_org_audience, topic=Topic.objects.get(name="Events & Deadlines")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
        try:
            context['campus_org_account_management_tutorials'] = tutorials.filter(audience__in = campus_org_audience, topic=Topic.objects.get(name="Account Management")).order_by("sort_order")
        except Topic.DoesNotExist:
            pass
    context['top_questions'] = filter_faq_questions(request.user, Question.objects.visible()).order_by("-click_count")[:s.TOP_QUESTIONS_NUM]
    context.update(extra_context or {})
    return context


@require_http_methods(["POST", "GET"])
@render_to('faq.html')
def faq(request, extra_context = None):
    if request.method == "POST":
        if not request.POST.has_key("question_id"):
            raise Http400("Request POST is missing 'question_id'.")
        q = Question.objects.get(id=request.POST["question_id"])
        q.click_count += 1
        q.save()
        return HttpResponse()
    else:
        context = {'topics':[]}
        for topic in Topic.objects.all():
            questions = filter_faq_questions(request.user, topic.question_set.visible())
            if questions:
                context['topics'].append({'name': topic, 'questions':questions})
        context.update(extra_context or {})  
        return context


@require_GET
@render_to()
def tutorial(request, slug, extra_context = None):
    tutorial = get_object_or_404(Tutorial, slug=slug)
    context = {
       'tutorial':tutorial,
       'TEMPLATE': 'tutorials/%s.html' % tutorial.slug.replace("-", "_")
    }
    if is_recruiter(request.user):
        context['other_recruiters'] = request.user.recruiter.employer.recruiter_set.exclude(id=request.user.recruiter.id)
    
    context.update(extra_context or {})
    return context


@require_http_methods(["POST", "GET"])
def landing_page_wrapper(request, extra_context=None):
    if request.user.is_authenticated():
        return home(request, extra_context=extra_context)
    else:
        return landing_page(request, extra_context=extra_context)


@require_http_methods(["POST", "GET"])
@render_to('landing_page.html')
def landing_page(request, extra_context = None):
    
    posted = False
    disabled = False
    form_error = False
    email_error = False
    loggedout = False

    if request.GET.get('action', None) == 'logged-out':
        loggedout = True
    
    recruiter_audience = [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_EMPLOYERS, core_enums.EMPLOYER, core_enums.CAMPUS_ORGS_AND_EMPLOYERS]
    tutorials = Tutorial.objects.filter(display=True, audience__in = recruiter_audience).order_by("sort_order")
    landing_page_tutorials = ["Find Candidates",
                              "Create & Deliver Resume Books",
                              "Browse RSVPs & Attendees",
                              "Create Events & Deadlines",
                              "Send Invitations",
                              "Create Account for Co-Workers",
                              "Publish Your Company Profile",
                              "Check Students In"]
    tutorials = tutorials.filter(action__in = landing_page_tutorials)
    
    employers = []
    for employer in Employer.objects.all():
        if (employer.logo) and employer.name != "Umeqo":
            employers.append(employer)
    context = {
        'student_reg_form': StudentRegistrationForm(),
        'posted': posted,
        'disabled': disabled,
        'loggedout': loggedout,
        'form_error': form_error,
        'email_error': email_error,
        'tutorials': tutorials,
        'employers': employers
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
    msg = request.GET.get('msg', None)
    if msg:
        context.update(msg = page_messages.get(msg))
    if request.user.is_staff:
        return HttpResponseRedirect(reverse("login"))
    if request.user.is_authenticated():
        if is_student(request.user):
            if not request.user.student.profile_created:
                return redirect('student_profile')
            subscriptions = [employer.id for employer in request.user.student.subscriptions.all()]
            event_sqs = get_upcoming_events_sqs(request.user).filter(SQ(attending_employers__in=subscriptions) | SQ(invitees=request.user.id))
            context.update(get_categorized_events_context(len(event_sqs)>0, event_sqs, request.user))
            context['has_subscriptions'] = len(subscriptions) > 0
            context['TEMPLATE'] = 'student_home.html'
        else:
            context.update(get_upcoming_events_context(request.user))
            if is_recruiter(request.user):
                context.update({
                    'search_form': StudentSearchForm(),
                    'notices': Notice.objects.notices_for(request.user),
                    'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                    'subscribers': Student.objects.filter(subscriptions__in=[request.user.recruiter.employer]).count()
                });
                context['TEMPLATE'] = 'employer_home.html'
            elif is_campus_org(request.user):
                context.update({
                    'notices': Notice.objects.notices_for(request.user),
                    'unseen_notice_num': Notice.objects.unseen_count_for(request.user),
                });
                context['TEMPLATE'] = 'campus_org_home.html'
        context.update(extra_context or {})
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


@require_GET
def check_website(request):
    if not request.GET.has_key("website"):
        raise Http400("Request GET is missing the website.")
    url_validator =  URLValidator(verify_exists = False)
    website = request.GET.get("website", "")
    try:
        url_validator(website)
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    except ValidationError:
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")


@require_GET
def check_password(request):
    if request.user.check_password(request.GET.get("password")):
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    else:
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")


@require_GET
def check_email_availability(request):
    if not request.GET.has_key("email"):
        raise Http400("Request GET is missing the email.")
    try:
        User.objects.get(email=request.GET["email"])
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    except User.DoesNotExist:
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")


@require_GET
@login_required
def check_event_name_uniqueness(request):
    if not request.GET.has_key("name"):
        raise Http400("Request GET is missing the name.")
    try:
        Event.objects.get(name=request.GET["name"])
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    except Event.DoesNotExist:
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")


@require_GET
@login_required
@render_to('course_info.html')
def course_info(request, extra_context = None):
    if not request.GET.has_key('course_id'):
        raise Http400("Request GET is missing 'course_id'.")
    id = request.GET['course_id']
    try:
        course = Course.objects.get(id = id)
    except Course.DoesNotExist:
        raise Http404("A course with id '%s' does not exist." % id)
    context = {'course':course}
    context.update(extra_context or {})
    return context  


@require_GET
@login_required
def check_language_uniqueness(request):
    if not request.GET.has_key("name"):
        raise Http400("Request GET is missing the name.")
    if Language.objects.filter(name=request.GET["name"]).exists():
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    else:
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")


@require_GET
@login_required
def get_notice_unseen_count(request):
    count = Notice.objects.unseen_count_for(request.user, on_site=True)
    return HttpResponse(simplejson.dumps({'count': count}), mimetype="application/json")

@requires_csrf_token
def handle_500(request, exception=None, extra_context = None):
    t = loader.get_template('500.html')
    context = {'exception':exception }
    if request.user.is_anonymous():
        context['login_form'] = AuthenticationForm
    context['request'] = request
    return HttpResponseServerError(t.render(RequestContext(request, context)))


@requires_csrf_token
def handle_404(request, exception=None, extra_context = None):
    t = loader.get_template('404.html')
    context = {'exception':exception }
    if request.user.is_anonymous():
        context['login_form'] = AuthenticationForm
    context['request'] = request
    return HttpResponseNotFound(t.render(RequestContext(request, context)))


@requires_csrf_token
def handle_403(request, exception=None, extra_context = None):
    t = loader.get_template('403.html')
    context = {'exception':exception }
    if request.user.is_anonymous():
        context['login_form'] = AuthenticationForm
    context['request'] = request
    return HttpResponseForbidden(t.render(RequestContext(request, context)))


@requires_csrf_token
def handle_400(request, exception=None, extra_context = None):
    t = loader.get_template('400.html')
    context = {'exception':exception }
    if request.user.is_anonymous():
        context['login_form'] = AuthenticationForm
    context['request'] = request
    return HttpResponseBadRequest(t.render(RequestContext(request, context)))