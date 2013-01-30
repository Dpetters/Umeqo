from __future__ import division
from __future__ import absolute_import

import datetime

from django.conf import settings as s
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.utils import simplejson
from django.template import Context
from django.template.loader import render_to_string
from ratelimit.decorators import ratelimit

from campus_org.forms import CreateCampusOrganizationForm
from campus_org.models import CampusOrg
from core import messages
from core.decorators import render_to
from core.email import get_basic_email_context, send_email
from core.forms import CreateLanguageForm
from core.http import Http403, Http400
from core.models import Language, EmploymentType, Industry, GraduationYear, Course
from core.email import is_valid_email
from countries.models import Country
from employer.decorators import is_recruiter
from employer.models import Employer
from employer.view_helpers import get_unlocked_students
from events.models import Attendee, RSVP, DroppedResume, Event
from notification.models import NoticeSetting, NoticeType, EMAIL
from registration.backend import RegistrationBackend
from registration.forms import PasswordChangeForm
from registration.view_helpers import register_student
from student.decorators import is_student
from student.forms import StudentAccountDeactivationForm, StudentPreferencesForm, StudentRegistrationForm, StudentUpdateResumeForm, StudentProfilePreviewForm, StudentProfileForm, StudentQuickRegistrationForm
from student.models import Student, StudentDeactivation, DegreeProgram
from student.view_helpers import handle_uploaded_file, extract_resume_keywords



@render_to('student_quick_registration.html')
@require_http_methods(["POST", "GET"])
def student_quick_registration(request, form_class=StudentQuickRegistrationForm, extra_context=None):
    context = {}
    if request.method == "POST":
        data = {}
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            pdf_file_path = "student/student/quick_reg_resume_%s.pdf" %(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            handle_uploaded_file(request.FILES['resume'], "%s%s" % (s.MEDIA_ROOT, pdf_file_path))
            
            # process_resume_data returns either an error or the keywords
            keywords, num =  extract_resume_keywords(pdf_file_path)
            
            # If the resume is not unparsable, then resume_parsing_results
            # contains the keywords
            if num == 0:
                data['unparsable_resume'] = True

            user_info =  {'username': request.POST['email'],
                          'first_name': request.POST['first_name'],
                          'last_name': request.POST['last_name'],
                          'email': request.POST['email'],
                          'password': request.POST['password']}
            student = register_student(request, **user_info)
            student.degree_program = DegreeProgram.objects.get(id=request.POST['degree_program'])
            student.graduation_month = request.POST['graduation_month']
            student.graduation_year = GraduationYear.objects.get(id=request.POST['graduation_year'])
            student.first_major = Course.objects.get(id=request.POST['first_major'])
            student.gpa = request.POST['gpa']
            file_content = file("%s%s" % (s.MEDIA_ROOT, pdf_file_path), "rb")
            student.resume.save(request.FILES['resume'].name, File(file_content))
            
            if keywords:
                student.keywords = keywords
            student.profile_created = True
            student.save()
            for attendee in Attendee.objects.filter(email=student.user.email):
                attendee.student = student
                attendee.save()
            event = Event.objects.get(id=request.POST['event_id'])
            action = request.POST['action']
            DroppedResume.objects.create(student=student, event=event)
            if action == "rsvp":
                RSVP.objects.create(student=student, event=event)
        else:
            data['errors'] = form.errors
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    if not request.GET.has_key('event_id'):
        raise Http400("Request GET is missing the event_id.")
    if not request.GET.has_key('action'):
        raise Http400("Request GET is missing the action.")
    context['form'] = form_class(initial={'event_id':request.GET['event_id'], 'action':request.GET['action']})
    action = request.GET['action']
    if action=="rsvp":
        context['action'] = "RSVP"
    elif action=="drop":
        context['action'] = "drop resume"
    context.update(extra_context or {})
    return context


@require_GET
@render_to('student_quick_registration_done.html')
def student_quick_registration_done(request, extra_context=None):
    context = {'unparsable_resume':request.GET.get("unparsable_resume", False)}
    context.update(extra_context or {})
    return context


@user_passes_test(is_student)
@render_to('student_profile_unparsable_resume.html')
def student_profile_unparsable_resume(request, extra_context=None):
    return {}


@require_GET
@user_passes_test(is_student)
@render_to("student_account.html")
def student_account(request, preferences_form_class = StudentPreferencesForm, 
                    change_password_form_class = PasswordChangeForm, 
                    extra_context=None):
    context = {}
    page_messages = {
        'password-changed': messages.password_changed,
    }
    msg = request.GET.get('msg', None)
    if msg:
        context["msg"] = page_messages[msg]
    
    context['preferences_form'] = \
    preferences_form_class(instance = request.user.student.studentpreferences)
    
    context['change_password_form'] = change_password_form_class(request.user)
    context.update(extra_context or {})
    return context


#@require_POST
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
def student_increment_resume_view_count(request):
    if not request.POST.has_key("student_id"):
        raise Http400("Request POST is missing the student_id.")
    student = Student.objects.get(id=request.POST['student_id'])
    if request.user.recruiter.employer.name != "Umeqo":
        student.studentstatistics.resume_view_count += 1
        student.studentstatistics.save()
    return HttpResponse()


@user_passes_test(is_student)
@render_to("student_account_deactivate.html")
def student_account_deactivate(request, form_class=StudentAccountDeactivationForm):
    if request.method == "POST":
        form = form_class(data = request.POST)
        if form.is_valid():
            data = []
            user = request.user
            student = user.student
            user.is_active = False
            user.save()
            for session_key in user.sessionkey_set.all():
                Session.objects.filter(session_key=session_key.session_key).delete()
            user.sessionkey_set.all().delete()
            student_deactivation = StudentDeactivation.objects.create(student = student)
            if form.cleaned_data.has_key('suggestion'):
                student_deactivation.suggestion = form.cleaned_data['suggestion']
                student_deactivation.save()
        else:
            data = {'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        context = {}
        context['form'] = form_class()
        return context


@require_POST
@user_passes_test(is_student)
def student_account_preferences(request, preferences_form_class = StudentPreferencesForm, extra_context = None):
    form = preferences_form_class(data = request.POST, instance = request.user.student.studentpreferences)
    if form.is_valid():
        request.user.student.student_preferences = form.save()
        
        public_invite = NoticeType.objects.get(label = "public_invite")
        private_invite = NoticeType.objects.get(label = "private_invite")
        new_event = NoticeType.objects.get(label = "new_event")
        
        try:
            n = NoticeSetting.objects.get(user=request.user, notice_type = public_invite, medium = EMAIL)
        except NoticeSetting.DoesNotExist:
            n = NoticeSetting.objects.create(user=request.user, notice_type = public_invite, medium = EMAIL)
        n.send = form.cleaned_data["email_on_invite_to_public_event"];
        n.save()
        
        try:
            n = NoticeSetting.objects.get(user=request.user, notice_type = private_invite, medium = EMAIL)
        except NoticeSetting.DoesNotExist:
            n = NoticeSetting.objects.create(user=request.user, notice_type = private_invite, medium = EMAIL)
        n.send = form.cleaned_data["email_on_invite_to_private_event"];
        n.save()
        
        try:
            n = NoticeSetting.objects.get(user=request.user, notice_type = new_event, medium = EMAIL)
        except NoticeSetting.DoesNotExist:
            n = NoticeSetting.objects.create(user=request.user, notice_type = new_event, medium = EMAIL)
        n.send = form.cleaned_data["email_on_new_subscribed_employer_event"];
        n.save()

        data = {'valid':True}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")    
    else:
        data = {'valid':False, 'form_errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@render_to("student_registration.html")
def student_registration(request, backend = RegistrationBackend(), form_class = StudentRegistrationForm, success_url = 'student_registration_complete', extra_context = None):
    if not backend.registration_allowed(request):
        return redirect('student_registration_closed')
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email']
            register_student(request, **form.cleaned_data)
            if request.is_ajax():
                data = {
                    'success_url': reverse(success_url),
                    'email': form.cleaned_data['email']
                }
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            return redirect(success_url)
        else:
            if request.is_ajax():
                data = {'errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class()
    context = {'form':form}
    context.update(extra_context or {}) 
    return context


@render_to('student_registration_complete.html')
def student_registration_complete(request, extra_context = None):
    email = request.GET.get('email', None)
    context = {'email': email}
    context.update(extra_context)
    return context


@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_profile.html")
def student_profile(request, form_class=StudentProfileForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
        if form.is_valid():
            student = form.save()
            if form.cleaned_data['sat_w'] != None and form.cleaned_data['sat_m'] != None and form.cleaned_data['sat_v'] != None:
                student.sat_t = int(form.cleaned_data['sat_w']) + int(form.cleaned_data['sat_v']) + int(form.cleaned_data['sat_m'])
            else:
                student.sat_t = None
            data = {'valid':True, 'unparsable_resume':False}
            if request.FILES.has_key('resume'):
                keywords, num = extract_resume_keywords(request.user.student.resume.name)
                student.keywords = keywords
                student.last_update = datetime.datetime.now()
                student.profile_created = True
                if num==0 and request.POST['ignore_unparsable_resume'] == "false":
                    data['unparsable_resume'] = True
                student.save()
                for a in Attendee.objects.filter(email=student.user.email):
                    a.student = student
                    a.save()
        else:
            data = {'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    else:
        form = form_class(instance=request.user.student)
        context = { 'form' : form,
                    'max_resume_size' : s.MAX_RESUME_SIZE,
                    'edit' : request.user.student.profile_created,
                    'industries_of_interest_max' : s.SP_MAX_INDUSTRIES_OF_INTEREST,
                    'campus_involvement_max': s.SP_MAX_CAMPUS_INVOLVEMENT,
                    'languages_max':s.SP_MAX_LANGUAGES,
                    'countries_of_citizenship_max':s.SP_MAX_COUNTRIES_OF_CITIZENSHIP,
                    'previous_employers_max':s.SP_MAX_PREVIOUS_EMPLOYERS,
                    'max_industries':s.EP_MAX_INDUSTRIES}
        context.update(extra_context or {})
        return context


@user_passes_test(is_student)
@render_to("student_profile_preview.html")
def student_profile_preview(request, form_class=StudentProfilePreviewForm, extra_context=None):
    form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
    print form.is_valid()
    if form.is_valid():
        student = form.save(commit=False)
        if form.cleaned_data['sat_w'] != None and form.cleaned_data['sat_m'] != None and form.cleaned_data['sat_v'] != None:
            student.sat_t = int(form.cleaned_data['sat_w']) + int(form.cleaned_data['sat_v']) + int(form.cleaned_data['sat_m'])
        else:
            student.sat_t = None
        
        context = {'student':student,
                   'edit' : request.user.student.profile_created,
                   'in_resume_book':False,
                   'starred':False,
                   'comment':messages.comment_text,
                   'num_of_events_attended':1,
                   'profile_preview':True}
        
        if request.POST.has_key('looking_for'):
            context['looking_for'] = EmploymentType.objects.filter(id__in=request.POST.getlist('looking_for'))
        if request.POST.has_key('industries_of_interest'):
            context['industries_of_interest'] = Industry.objects.filter(id__in=request.POST.getlist('industries_of_interest'))
        if request.POST.has_key('previous_employers'):
            context['previous_employers'] = Employer.objects.filter(id__in=request.POST.getlist('previous_employers'))
        if request.POST.has_key('campus_involvement'):
            context['campus_involvement'] = CampusOrg.objects.filter(id__in=request.POST.getlist('campus_involvement'))
        if request.POST.has_key('languages'):
            context['languages'] = Language.objects.filter(id__in=request.POST.getlist('languages'))
        if request.POST.has_key('countries_of_citizenship'):
            context['countries_of_citizenship'] = Country.objects.filter(iso__in=request.POST.getlist('countries_of_citizenship'))
                            
        context.update(extra_context or {})
        return context
    else:
        if form.non_field_errors():
            error_html = form.non_field_errors()[0]
        else:
            for field in form:
                if field.errors:
                    error_html = field.errors[0]
                    break
        return HttpResponse("<div class='message_section'>%s</div>" % error_html)


@require_http_methods(["POST"])
@user_passes_test(is_student)
def student_update_resume(request, form_class=StudentUpdateResumeForm):
    form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
    if form.is_valid():
        form.save()
        data = {}
        student = request.user.student 
        keywords, num = extract_resume_keywords(student.resume.name)
        if num == 0:
            data['unparsable_resume'] = True
        data['num_of_extracted_keywords'] = num
        student.keywords = keywords
        student.last_updated = datetime.datetime.now()
        student.save()
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        data = {'errors': form.errors }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@require_http_methods(["GET"])
@user_passes_test(is_student)
def student_update_resume_info(request):
    num = len(filter(None, request.user.student.keywords.split(" ")))
    data = {'num_of_extracted_keywords' : num}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@user_passes_test(is_student)
@render_to("student_create_campus_org.html")
def student_create_campus_org(request, form_class=CreateCampusOrganizationForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            new_campus_org = form.save()
            recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
            
            context = Context({'first_name':request.user.student.first_name, \
                               'last_name':request.user.student.last_name, \
                               'email':request.user.email, \
                               'new_campus_org':new_campus_org})
            context.update(get_basic_email_context())
            
            txt_email_body = render_to_string('new_campus_org_email_body.txt', context)
            
            subject = ''.join(render_to_string('email_admin_subject.txt', {
                'message': "New Campus Org: %s" % new_campus_org
            }, context).splitlines())

            send_email(subject, txt_email_body, recipients)
            
            data = {"type": new_campus_org.type.name,
                    "name": new_campus_org.name,
                    "id": new_campus_org.id}
        else:
            data = {'errors': form.errors }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class()
    context =  {'form': form }
    context.update(extra_context or {}) 
    return context


@user_passes_test(is_student)
@render_to("student_create_language.html")
def student_create_language(request, form_class=CreateLanguageForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            new_language_name = form.cleaned_data['name']
            basic = Language.objects.create(name_and_level=new_language_name + " (Basic)", name=new_language_name)
            proficient = Language.objects.create(name_and_level=new_language_name + " (Proficient)", name=new_language_name)
            fluent = Language.objects.create(name_and_level=new_language_name + " (Fluent)", name=new_language_name)
            recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
            
            context = Context({'first_name':request.user.student.first_name, \
                                'last_name':request.user.student.last_name, \
                                'email':request.user.email, \
                                'new_language':new_language_name})
            context.update(get_basic_email_context())
             
            body = render_to_string('new_language_email_body.txt', context)
            
            subject = ''.join(render_to_string('email_admin_subject.txt', {
                'message': "New Language: %s" % new_language_name
            }, context).splitlines())
                        
            send_email(subject, body, recipients)
            
            data = {"name":new_language_name, 
                    "fluent_id":fluent.id, 
                    "proficient_id":proficient.id, 
                    "basic_id":basic.id}  
        else:
            data = {'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class()
        
    context =  { 'form': form }
    context.update(extra_context or {})
    return context


@user_passes_test(is_student)
def student_resume(request):
    resume = request.user.student.resume.read()
    response = HttpResponse(resume, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s_%s.pdf' % (request.user.last_name.lower(), request.user.first_name.lower())
    return response


@require_GET
@user_passes_test(is_recruiter)
@ratelimit(rate='30/m')
def specific_student_resume(request, student_id):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        raise Http403("You have exceeded the resume viewing per minute limit. " +
                      "Please wait before trying again and consider using the resume book tool for collecting resumes in batches.")
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise Http404("A student with the id %s does not exist." % student_id)
    employer = request.user.recruiter.employer
    if not student in get_unlocked_students(employer, request.META['has_at_least_premium']):
        raise Http403("You have not unlocked this student yet and thus can't view their resume. To unlock him/her either upgrade your subscription or have him/her RSVP to or attend one of your events.")
    resume = student.resume.read()
    response = HttpResponse(resume, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s_%s_%s.pdf' % (student.id, student.user.last_name.lower(), student.user.first_name.lower())
    return response
