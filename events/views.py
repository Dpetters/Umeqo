from __future__ import division
from __future__ import absolute_import

import cStringIO as StringIO
from datetime import datetime, timedelta
import re

from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from django.template import RequestContext, loader
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.shortcuts import redirect, render_to_response
from django.template.loader import render_to_string


from campus_org.models import CampusOrg
from employer.models import Employer
from core.email import send_html_mail
from core import enums as core_enums
from core.http import Http403, Http400, Http500
from core.decorators import agreed_to_terms, is_recruiter, is_student, is_campus_org_or_recruiter, is_campus_org, render_to, has_annual_subscription, has_any_subscription
from core.models import Edit
from core.view_helpers import english_join
from events.forms import EventForm, CampusOrgEventForm, EventExportForm, EventFilteringForm
from events.models import Attendee, Event, EventType, Invitee, RSVP, DroppedResume, notify_about_event
from events.view_helpers import event_map, event_filtering_helper, get_event_schedule, get_attendees, get_invitees, get_rsvps, get_no_rsvps, get_dropped_resumes, export_event_list_csv, export_event_list_text
from notification import models as notification
from student.models import Student


@login_required
@agreed_to_terms
def events(request, category, extra_context=None):
    context = {'category':category}
    if category=="past":
        context['past'] = True
    if category=="archived":
        context['archived'] = True
    # We do a special thing for upcoming events to display them as "Today", "Tomorrow", "This week"
    if category =="upcoming":
        context.update(event_filtering_helper(category, request))
    else:
        events_exist, events = event_filtering_helper(category, request)
        context['events_exist'] = events_exist
        context['events'] = events
    if request.is_ajax():
        template = loader.get_template("event_filtering_results.html")
        response = HttpResponse(template.render(RequestContext(request, context)))
        # Need the no-store header because of chrome history api bug
        # see http://stackoverflow.com/questions/8240710/chrome-history-api-problems
        response['Cache-Control'] = "no-store"
        return response
    else:
        if request.GET.has_key("query"):
            context['initial_state'] = simplejson.dumps(request.GET)
            context['event_filtering_form'] = EventFilteringForm(request.GET)
        else:
            context['event_filtering_form'] = EventFilteringForm()
        if is_campus_org_or_recruiter(request.user):
            template = "events_employer_campus_org.html"
        elif is_student(request.user):
            if not request.user.student.profile_created:
                return redirect('student_profile')
            template = "events_student.html"
    return render_to_response(template, context, context_instance=RequestContext(request) )


@require_GET
@login_required
@user_passes_test(is_campus_org_or_recruiter)
def events_check_short_slug_uniqueness(request):
    if not request.GET.has_key("short_slug"):
        raise Http400("Request GET is missing the short_slug.")
    data = {'used':False}
    if is_campus_org(request.user):
        if Event.objects.filter(short_slug = request.GET['short_slug'], owner=request.user).exists():
            data['used'] = True
    elif is_recruiter(request.user):
        if Event.objects.filter(short_slug = request.GET['short_slug'], owner__recruiter__employer=request.user.recruiter.employer).exists():
            data['used'] = True
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@require_GET
@agreed_to_terms
def events_shortcut(request, owner_slug, event_slug, extra_context=None):
    try:
        employer = Employer.objects.get(slug = owner_slug)
        events = reduce(lambda a,b: [a, a.extend(b.user.event_set.all().order_by("-date_created"))][0], employer.recruiter_set.all(), [])
    except Employer.DoesNotExist:
        try:
            campus_org = CampusOrg.objects.get(slug = owner_slug)
            events = campus_org.user.event_set.all().order_by("-date_created")
        except CampusOrg.DoesNotExist:
            raise Http404("Employer or Campus Organization with slug '%s' does not exist." % owner_slug)
    if events != []:
        try:
            slug_matches = filter(lambda a: a.short_slug == event_slug, events)
            if slug_matches:
                url = slug_matches[0].get_absolute_url()
                if url:
                    return redirect(url)
        except Event.DoesNotExist:
            pass
    raise Http404("Event with slug '%s' does not exist." % event_slug)


def event_page_redirect(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        raise Http404("Event with id '%s' does not exist." % id)
    return redirect("%s" % (event.get_absolute_url()))


@render_to('event_page.html')
@agreed_to_terms
def event_page(request, id, slug, extra_context=None):
    if is_student(request.user) and not request.user.student.profile_created:
        return redirect('student_profile')
    try:
        event = Event.objects.get(pk=id)
    except:
        raise Http404("Event with id '%s' does not exist." % id)
    if not event.is_public:
        if not request.user.is_authenticated():
            raise Http403("This event is private. You do not have permission to view it.")
        elif is_campus_org(request.user):
            if request.user != event.owner:
                raise Http403("This event is private. You do not have permission to view it.")
        elif is_recruiter(request.user):
            if request.user != event.owner and request.user.recruiter.employer not in event.attending_employers.all():
                raise Http403("This event is private. You do not have permission to view it.")
        elif is_student(request.user):
            try:
                Invitee.objects.get(event=event, student=request.user.student)
            except:
                raise Http403("This event is private. You do not have permission to view it.")

    current_site = Site.objects.get(id=s.SITE_ID)

    page_url = 'http://' + current_site.domain + event.get_absolute_url()
    #google_description is the description + stuff to link back to umeqo
    google_description = event.description + '\n\nRSVP and more at %s' % page_url
    
    context = {
        'page_url': page_url,
        'DOMAIN': current_site.domain,
        'current_site':"http://" + current_site.domain,
        'google_description': google_description
    }
        
    if len(event.audience.all()) > 0:
        context['audience'] = event.audience.all()
    
    if is_campus_org(event.owner):
        context['campus_org_event'] = True
        context['attending_employers'] = event.attending_employers
        if is_campus_org(request.user):
            context['can_edit'] = (event.owner == request.user)
            context['show_admin'] = (event.owner == request.user)
        elif is_recruiter(request.user):
            context['show_admin'] = request.user.recruiter.employer in event.attending_employers.all()
    elif is_recruiter(event.owner):
        if is_recruiter(request.user):
            context['can_edit'] = request.user.recruiter in event.owner.recruiter.employer.recruiter_set.all() and request.user.recruiter.employer.subscribed()
            context['show_admin'] = request.user.recruiter in event.owner.recruiter.employer.recruiter_set.all() and request.user.recruiter.employer.subscribed()
    
    if context.has_key('show_admin'):
        attendees = get_attendees(event)
        rsvps =  get_rsvps(event)
        context['invitees'] = get_invitees(event)
        
        if event.is_drop:
            dropped_resumes = get_dropped_resumes(event)
        else:
            dropped_resumes = []

        if not event.is_public:
            no_rsvps = get_no_rsvps(event)
        else:
            no_rsvps = []
            
        context.update({
        'rsvps':rsvps,
        'no_rsvps': no_rsvps,
        'dropped_resumes': dropped_resumes,
        'attendees': attendees
        });
    
    # Increase the view count if we're not admin, a campus org or a recruiter (aka for now just student & anonymous)
    if is_campus_org(request.user) and not is_recruiter(request.user) and not request.user.is_staff:
        event.view_count += 1
        event.save()
    
    if is_student(request.user):
        responded, attending, dropped_resume, attended, event = event_map(event, request.user)
        context['responded'] = responded
        context['attending'] = attending
        context['dropped_resume'] = dropped_resume
        context['attended'] = attended
    else:
        context['email_delivery_type'] = core_enums.EMAIL
    context['event'] = event
    context.update(extra_context or {})
    return context


@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@agreed_to_terms
@render_to("event_form.html")
def event_new(request, form_class=None, extra_context=None):
    context = {}
    if is_recruiter(request.user):
        employer = request.user.recruiter.employer
        form_class = EventForm
    elif is_campus_org(request.user):
        form_class = CampusOrgEventForm
        context['max_industries'] = s.EP_MAX_INDUSTRIES
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            form.save_m2m()
            if event.type.name == "Rolling Deadline":
                event.start_datetime = datetime.now() - timedelta(weeks=1)
                event.end_datetime = datetime.now() + timedelta(weeks=1000)
                event.save()
            elif event.type.name == "Hard Deadline":
                event.start_datetime = event.end_datetime
                event.save()
            if is_recruiter(request.user):
                event.attending_employers.add(employer)
                # Update index
                employer.save()
            notify_about_event(event, "new_event", event.attending_employers.all())
            # Update index
            event.save()
            return HttpResponseRedirect(reverse('event_page', kwargs={'id':event.id, 'slug':event.slug}))
    else:
        form = form_class(initial={
            'start_datetime': datetime.now() + timedelta(minutes=30),
            'end_datetime': datetime.now() + timedelta(hours=1, minutes=30),
        })
    context['hours'] = map(lambda x,y: str(x) + y, [12] + range(1,13) + range(1,12), ['am']*12 + ['pm']*12)
    context['form'] = form
    context['today'] = datetime.now().strftime('%m/%d/%Y')
    context['event_scheduler_date'] = datetime.now().strftime('%m/%d/%Y')
    context.update(extra_context or {})
    return context


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
def event_list_download(request):
    if not request.GET.has_key("event_id"):
        raise Http400("Request GET is missing the event_id.")
    try:
        event = Event.objects.get(id=request.GET["event_id"])
    except Event.DoesNotExist:
        raise Http404("Event with the id %d" % request.GET['event_id'])
    else:
        list = request.GET['event_list']
        if not request.GET.has_key('export_format'):
            raise Http400("The request is missing the file format.")
        if request.GET['export_format'] == core_enums.CSV:
            response = HttpResponse(mimetype='text/csv')
            filename = "%s.csv" % export_event_list_csv(response, event, list)
        #elif request.GET['export_format'] == core_enums.XLS:
        #    response = HttpResponse(mimetype="application/ms-excel")
        #    filename = export_event_list_xls(response, event, list)
        elif request.GET['export_format'] == core_enums.TEXT:
            response = HttpResponse(mimetype="text/plain")
            filename = "%s.txt" % export_event_list_text(response, event, list)
        else:
            raise Http500("The file format % isn't one we support." % request.GET['export_format'])
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response


@login_required
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
def event_checkin_count(request):
    data = {'count':len(Event.objects.get(id=request.GET["event_id"]).attendee_set.all())}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    

@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@render_to('event_list_export_completed.html')
def event_list_export_completed(request, extra_context = None):
    if not request.GET.has_key("event_list"):
        raise Http400("Filename is missing from the request.")
    if not request.GET.has_key("event_id"):
        raise Http400("Request GET is missing the event_id.")
    id = request.GET["event_id"]
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Http404("Event with the id %s does not exist." % id)
    list = request.GET['event_list']
    if list == "all":
        filename = "%s Respondees" % (event.name)
    elif list == "rsvps":
        filename = "%s RSVPs" % (event.name)
    elif list == "dropped_resumes":
        filename = "%s Resume Drops" % (event.name)
    elif list == "attendees":
        filename = "%s Attendees" % (event.name)    
    context = {'filename':filename}
    context.update(extra_context or {})
    return context


@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@render_to()
def event_list_export(request, form_class = EventExportForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            format = form.cleaned_data["export_format"]
            event = Event.objects.get(id=form.cleaned_data["event_id"])
            list = form.cleaned_data['event_list']
            reg = re.compile(r"\s*[;, \n]\s*")
            recipients = reg.split(request.POST['emails'])
            subject = ''.join(render_to_string('event_list_export_email_subject.txt', {}).splitlines())
            body = render_to_string('event_list_export_email_body.html', {'name':request.user.first_name})
            file = StringIO.StringIO()
            if format == core_enums.CSV:
                filename = export_event_list_csv(file, event, list)
                extension = "csv"
                file_contents = file.getvalue()
                mimetype = "text/csv"
            #elif format == core_enums.XLS:
            #    filename = export_event_list_xls(file, event, list)
            #    file_contents = file.getvalue()
            #    mimetype = "application/vnd.ms-excel"
            elif format == core_enums.TEXT:
                filename = export_event_list_text(file, event, list)
                extension = "txt"
                file_contents = file.getvalue()
                mimetype = "text/plain"
            else:
                raise Http500("The request format '%s' is not supported" % format)
            send_html_mail(subject, body, recipients, "%s.%s" % (filename, extension), file_contents, mimetype)
            context = {'filename': filename, 'TEMPLATE':'event_list_export_completed.html'}
            context.update(extra_context or {})
            return context
        else:
            data = {'errors':form.errors}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class(initial={'emails':request.user.email, 'event_id':request.GET['event_id'], 'event_list':request.GET['event_list']})
    context = {'form': form, 'TEMPLATE':'event_list_export.html'}
    context.update(extra_context or {}) 
    return context


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@render_to("event_form.html")
def event_edit(request, id=None, extra_context=None):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        raise Http404("Event with id '%s' does not exist." % id)
    
    context = {'event': event}
    if not admin_of_event(event, request.user):
        raise Http403('You are not allowed to edit this event.')  
    if is_recruiter(event.owner):
        form_class = EventForm
    elif is_campus_org(event.owner):
        context['max_industries'] = s.EP_MAX_INDUSTRIES
        context['attending_employers'] = event.attending_employers
        form_class = CampusOrgEventForm
    if request.method == 'POST':
        form = form_class(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.edits.add(Edit.objects.create(user=request.user))
            for employer in event.attending_employers.all():
                event.previously_attending_employers.add(employer)
            event.save()
            form.save_m2m()
            # Update index
            event.save()
            notify_about_event(event, "new_event", [e for e in list(event.attending_employers.all()) if e not in list(event.previously_attending_employers.all())])
            return HttpResponseRedirect(reverse('event_page', kwargs={'id':event.id, 'slug':event.slug}))
    else:
        form = form_class(instance=event)
    context['edit'] = True
    context['hours'] = map(lambda x,y: str(x) + y, [12] + range(1,13) + range(1,12), ['am']*12 + ['pm']*12)
    context['form'] = form
    context['today'] = datetime.now().strftime('%m/%d/%Y')
    if event.type.name == "Hard Deadline":
        context['event_scheduler_date'] = event.end_datetime.strftime('%m/%d/%Y')
    elif event.type.name == "Rolling Deadline":
        context['event_scheduler_date'] = datetime.now().strftime('%m/%d/%Y')
    else:
        context['event_scheduler_date'] =  event.start_datetime.strftime('%m/%d/%Y')
    context.update(extra_context or {})
    return context


def admin_of_event(event, user):
    if is_recruiter(event.owner):
        return is_recruiter(user) and user.recruiter.employer == event.owner.recruiter.employer
    elif is_campus_org(event.owner):
        return is_campus_org(user) and user.campusorg == event.owner.campusorg
    return False


@login_required
@agreed_to_terms
@has_annual_subscription
@user_passes_test(is_campus_org_or_recruiter)
@render_to("event_cancel_dialog.html")
def event_cancel(request, id, extra_context = None):
    if request.method == "POST":
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404("Event with id '%s' does not exist." % id)
        else:
            if not admin_of_event(event, request.user):
                raise Http403('You are not allowed to delete this event.')
            event.cancelled = True

            # Notify RSVPS.
            rsvps = map(lambda n: n.student.user, event.rsvp_set.all())
            employers = event.attending_employers.all()
            has_word = "has" if len(employers)==1 else "have"
            employer_names = english_join(map(lambda n: n.name, employers))
            notification.send(rsvps, 'cancelled_event', {
                'employer_names': employer_names,
                'has_word': has_word,
                'event': event
            })
            
            event.save()
            
            data = {}
            if event.is_deadline():
                data['type'] = "deadline"
            else:
                data['type'] = "event"
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404("Event with id '%s' does not exist." % id)
        context = {'event':event}
        context.update(extra_context or {})
        return context

    
@login_required
@agreed_to_terms
@has_annual_subscription
@require_POST
@user_passes_test(is_campus_org_or_recruiter)
def event_archive(request, id, extra_context = None):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise Http404("Event with id '%s' does not exist." % id)
    else:
        if not admin_of_event(event, request.user):
            raise Http403('You are not allowed to arhive this event.')
        event.archived = True
        event.save()
        data = {}
        if event.is_deadline():
            data['type'] = "deadline"
        else:
            data['type'] = "event"
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@login_required
@agreed_to_terms
@has_annual_subscription
@user_passes_test(is_campus_org_or_recruiter)
@render_to("rolling_deadline_end_dialog.html")
def rolling_deadline_end(request, id, extra_context = None):
    if request.method == "POST":
        try:
            event = Event.objects.get(pk=id)
        except Event.DoesNotExist:
            raise Http404("Event with id '%s' does not exist." % id)
        else:
            if not event.is_rolling_deadline():
                raise Http403('You cannot end anything other than a rolling deadline.')
            if is_recruiter(event.owner):
                if not is_recruiter(request.user) or request.user.recruiter.employer != event.owner.recruiter.employer:
                    raise Http403('You are not allowed to end this rolling deadline.')
            elif is_campus_org(event.owner):
                if not is_campus_org(request.user) or request.user.campusorg != event.owner.campusorg:
                    raise Http403('You are not allowed to end this rolling deadline.')
            event.end_datetime = datetime.now()-timedelta(minutes=1)
            event.save()
            return HttpResponse()
    else:
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404("Event with id '%s' does not exist." % id)
        context = {'event':event}
        context.update(extra_context or {})
        return context


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
def event_schedule(request):
    schedule = get_event_schedule(request.GET.get('event_date', datetime.now().strftime('%m/%d/%Y')), request.GET.get('event_id', None))
    return HttpResponse(simplejson.dumps(schedule), mimetype="application/json")


@login_required
@agreed_to_terms
@require_http_methods(["GET", "POST"])
@has_any_subscription
def event_rsvp(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except:
        raise Http404("Event with id '%s' does not exist." % event_id)
    else:
        # if method is GET then get a list of RSVPed students
        if request.method == 'GET' and is_campus_org_or_recruiter(request.user):
            data = map(lambda n: {'id': n.student.id, 'email': n.student.user.email}, event.rsvp_set.all())
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        # if POST then record student's RSVP
        elif request.method == 'POST' and is_student(request.user):
            isAttending = request.POST.get('attending', 'true')
            isAttending = True if isAttending=='true' else False
            rsvp, created = RSVP.objects.get_or_create(student=request.user.student, event=event)
            rsvp.attending = isAttending
            rsvp.save()
            if isAttending:
                DroppedResume.objects.get_or_create(event=event, student=request.user.student)
            if request.is_ajax():
                return HttpResponse()
            else:
                return redirect(reverse('event_page',kwargs={'id':id,'slug':event.slug}))
        else:
            raise Http403("You do not have access to this view.")

@login_required
@agreed_to_terms
@user_passes_test(is_student)
@require_POST
def event_drop(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event with id %d does not exist." % event_id)
    if not request.POST.has_key("drop"):
        raise Http400("Request POST is missing the boolean drop.")
    if request.POST["drop"]=="true":
        DroppedResume.objects.get_or_create(event=event, student=request.user.student)
    else:
        DroppedResume.objects.filter(event=event, student=request.user.student).delete()
    return HttpResponse()


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_annual_subscription
@require_GET
def event_raffle_winner(request, extra_context=None):
    if not request.GET.has_key("event_id"):
        raise Http400("Request GET is missing the event_id")
    data = {}
    winners = Attendee.objects.filter(event__id=request.GET['event_id'], won_raffle=False)
    if winners.exists():
        winner = winners[0]
        winner.won_raffle = True
        winner.save()
        if winner.student:
            winner.student.studentstatistics.raffles_won += 1
            winner.student.studentstatistics.save()
        data['name'] = winner.name
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required
@agreed_to_terms
@user_passes_test(is_campus_org_or_recruiter)
@has_any_subscription
@require_http_methods(["GET", "POST"])
def event_checkin(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'GET':
        return HttpResponse(simplejson.dumps(get_attendees(event)), mimetype="application/json")
    else:
        email = request.POST.get('email', None).strip()
        if not email:
            data = {
                'valid': False,
                'error': 'Enter a valid email!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        name = request.POST.get('name', None)
        student = None
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if hasattr(user, 'student'):
                student = user.student
        if not name and not student:
            data = {
                'valid': False,
                'error': "This email isn't registered with Umeqo. Enter your name!"
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if Attendee.objects.filter(event=event, email=email).exists():
            data = {
                'valid': False,
                'error': 'Duplicate checkin!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if not name:
            name = "%s %s" % (user.student.first_name, user.student.last_name)
        attendee = Attendee(email=email, name=name, student=student, event=event)
        try:
            attendee.save()
        except IntegrityError:
            data = {
                'valid': False,
                'error': 'Duplicate checkin!'
            }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if not student or student and not student.profile_created:
            if not student:
                template = 'checkin_follow_up.html'
            if student and not student.profile_created:
                template = 'checkin_follow_up_profile.html'
            subject = "[Umeqo] Event Check-In Follow-up"
            recipients = [email]
            body_context = {'name':name, 'current_site':Site.objects.get(id=s.SITE_ID), 'event':event, 'campus_org_event': is_campus_org(event.owner)}
            html_body = render_to_string(template, body_context)
            send_html_mail(subject, html_body, recipients)
        output = {
            'valid': True,
            'email': email
        }
        if student:
            output['name'] = student.first_name + ' ' + student.last_name
        else:
            output['name'] = name
        return HttpResponse(simplejson.dumps(output), mimetype="application/json")


@login_required
@agreed_to_terms
@user_passes_test(is_student)
@require_GET
@render_to("event_rsvp_message_dialog.html")
def event_rsvp_message(request, extra_context=None):
    if not request.GET.has_key("event_id"):
        raise Http403("Request GET is missing the event_id.")
    id = request.GET['event_id']
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise Http404("Event with id '%s' does not exist." % id)
    context = {}
    if event.rsvp_message:
        context['event'] = event
        if is_campus_org(event.owner):
            context['is_campus_org_event'] = True
        return context
    return HttpResponse()


@login_required
@agreed_to_terms
@user_passes_test(is_recruiter)
@has_annual_subscription
def events_by_employer(request):
    events = Event.objects.filter(Q(owner=request.user) | Q(attending_employers__in=[request.user.recruiter.employer])).filter(end_datetime__gte=datetime.now()).order_by("end_datetime")
    student_id, student = request.GET.get('student_id', None), None
    if student_id and not Student.objects.filter(id=student_id).exists():
        raise Http404("Student with %d does not exist." % student_id)
    elif student_id:
        student = Student.objects.get(id=student_id)
    def eventMap(event):
        invited = False
        if student and Invitee.objects.filter(event=event, student=student).exists():
            invited = True
        return {
            'id': event.id,
            'name': event.name,
            'is_public': event.is_public,
            'invited': invited,
        }
    return HttpResponse(simplejson.dumps(map(eventMap, events)), mimetype="application/json")


@login_required
@agreed_to_terms
@user_passes_test(is_recruiter)
@has_annual_subscription
@require_POST
def event_invite(request):
    event_id = request.POST.get('event_id', None)
    student_ids = request.POST.get('student_ids', None)
    message = request.POST.get('message', None)
    if not (event_id and student_ids and message):
        data = { 'valid': False, 'message': 'Missing data!' }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    event = Event.objects.filter(id=event_id)
    if not event.exists():
        data = { 'valid': False, 'message': 'Invalid event!' }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    event = event.get()
    student_ids = student_ids.split('~')
    students = []
    for student_id in student_ids:
        student = Student.objects.filter(id=student_id)
        if not student.exists():
            data = { 'valid': False, 'message': 'Invalid students.' }
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        students.append(student.get())
    for student in students:
        invitee = Invitee.objects.filter(event=event, student=student)
        if invitee.exists():
            invitee = invitee.get()
            invitee.datetime_created = datetime.now()
            invitee.save()
        else:
            Invitee.objects.create(event=event, student=student)
        employer = request.user.recruiter.employer
        # Update Index
        event.save()
        if event.is_public:
            notice_type = 'public_invite'
        else:
            notice_type = 'private_invite'
        notification.send([student.user], notice_type, {
            'name': student.user.first_name,
            'recruiter': request.user,
            'employer': employer,
            'event': event,
            'invite_message': message,
            'time_added': datetime.now(),
            'message': '<strong>%s</strong> has invited you to their event: "%s"' % (employer.name, event.name),
        })
    data = { 'valid': True, 'message': 'Invite sent successfully.' }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")