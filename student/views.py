from __future__ import division
from __future__ import absolute_import

from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.utils import simplejson
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from notification.models import NoticeSetting, NoticeType, EMAIL
from student.forms import StudentAccountDeactivationForm, StudentPreferencesForm, StudentRegistrationForm, StudentUpdateResumeForm,\
                            StudentProfilePreviewForm, StudentProfileForm, BetaStudentRegistrationForm
from student.models import Student, StudentDeactivation, StudentInvite
from student.view_helpers import process_resume
from registration.forms import PasswordChangeForm
from registration.backend import RegistrationBackend
from core.decorators import is_student, render_to
from core.forms import CreateLanguageForm
from campus_org.forms import CreateCampusOrganizationForm
from core.models import Language, EmploymentType, Industry
from campus_org.models import CampusOrg
from core import messages
from employer.models import Employer
from student.enums import RESUME_PROBLEMS
from countries.models import Country
        

@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_account.html")
def student_account(request, preferences_form_class = StudentPreferencesForm, 
                    change_password_form_class = PasswordChangeForm, 
                    extra_context=None):
    
    if not request.user.student.profile_created:
        return redirect('student_profile')
    
    if request.method == "GET":
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
    else:
        return HttpResponseForbidden("Request must be a GET")


@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_account_deactivate.html")
def student_account_deactivate(request, form_class=StudentAccountDeactivationForm):

    if request.is_ajax():
        if request.method == "POST":
            form = form_class(data = request.POST)
            if form.is_valid():
                user = request.user
                student = user.student
                user.is_active = False
                user.save()
                for sk in user.sessionkey_set.all():
                    Session.objects.filter(session_key=sk.session_key).delete()
                user.sessionkey_set.all().delete()
                sd = StudentDeactivation.objects.create(student = student)
                if form.cleaned_data.has_key('suggestion'):
                    sd.suggestion = form.cleaned_data['suggestion']
                    sd.save()
                return HttpResponse(simplejson.dumps({}), 
                                    mimetype="application/json")
            else:
                if request.is_ajax():
                    return HttpResponse(simplejson.dumps({'errors':form.errors}), 
                                        mimetype="application/json")
        else:
            context = {}
            context['form'] = form_class()
            return context
    else:
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest") 


@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_account_preferences(request, preferences_form_class = StudentPreferencesForm, 
                                extra_context = None):
    if request.is_ajax():
        if request.method == "POST":
            form = preferences_form_class(data = request.POST, \
                                          instance = request.user.student.studentpreferences)

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
                data = {'valid':False,
                        'form_errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            return HttpResponseForbidden("Request must be a POST.")
    else:
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@render_to("student_registration.html")
def student_registration(request, backend = RegistrationBackend(), 
                         extra_context = None):
    if s.INVITE_ONLY:
        form_class = BetaStudentRegistrationForm
    else:
        form_class = StudentRegistrationForm

    success_url = 'student_registration_complete'
    if not backend.registration_allowed(request):
        return redirect('student_registration_closed')
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email']
            new_user = backend.register(request, **form.cleaned_data)
            student = Student(user=new_user)
            umeqo = Employer.objects.get(name="Umeqo")
            student.save()
            student.subscriptions.add(umeqo)
            student.save()
            if s.INVITE_ONLY:
                i=StudentInvite.objects.get(code=form.cleaned_data['invite_code'])
                i.recipient = student
                i.used = True
                i.save()
            if request.is_ajax():
                data = {
                    'valid': True,
                    'success_url': reverse(success_url),
                    'email': form.cleaned_data['email']
                }
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            return redirect(success_url)
        else:
            if request.is_ajax():
                data = {'valid':False, 'errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        if s.INVITE_ONLY and request.GET.has_key("ic"):
            form = form_class(initial={"invite_code":request.GET["ic"]})
        else:
            form = form_class()
    
    context = {'form':form, 'debug':s.DEBUG}
    context.update(extra_context or {}) 
    return context


def student_registration_complete(request,
            template_name='student_registration_complete.html',
            extra_context = None):
    email = request.GET.get('email', None)
    context = {'email': email}
    context.update(extra_context)
    return render_to_response(template_name, context,
            context_instance = RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_profile.html")
def student_profile(request,
                     form_class=StudentProfileForm,
                     extra_context=None):

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
                resume_status = process_resume(request.user.student)
                if resume_status == RESUME_PROBLEMS.HACKED:
                    data = {'valid':False}
                    errors = {'resume': messages.resume_problem}
                    data['errors'] = errors
                elif resume_status == RESUME_PROBLEMS.UNPARSABLE and request.POST['ingore_unparsable_resume'] == "false":
                    data = {'valid':False}
                    data['unparsable_resume'] = True
            if data['valid'] and not data['unparsable_resume']:
                student.profile_created = True
                student.save()
        else:
            data = {'valid':False,
                    'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    else:
        form = form_class(instance=request.user.student)
        context = { 'form' : form,
                    'edit' : request.user.student.profile_created,
                    'industries_of_interest_max' : s.SP_MAX_INDUSTRIES_OF_INTEREST,
                    'campus_involvement_max': s.SP_MAX_CAMPUS_INVOLVEMENT,
                    'languages_max':s.SP_MAX_LANGUAGES,
                    'countries_of_citizenship_max':s.SP_MAX_COUNTRIES_OF_CITIZENSHIP,
                    'previous_employers_max':s.SP_MAX_PREVIOUS_EMPLOYERS}
        context.update(extra_context or {})
        return context


@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_profile_preview.html")
def student_profile_preview(request, form_class=StudentProfilePreviewForm,
                            extra_context=None):
    if request.user.is_authenticated() and hasattr(request.user, "student"):
        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
            if form.is_valid():
                student = form.save(commit=False)
                if form.cleaned_data['sat_w'] != None and form.cleaned_data['sat_m'] != None and form.cleaned_data['sat_v'] != None:
                    student.sat_t = int(form.cleaned_data['sat_w']) + int(form.cleaned_data['sat_v']) + int(form.cleaned_data['sat_m'])
                else:
                    student.sat_t = None
                
                context = {'student':student,
                           'in_resume_book':False,
                           'starred':False,
                           'comment':messages.comment_text,
                           'num_of_events_attended':1,
                           'profile_preview':True}
                
                if request.POST.has_key('multiselect_id_looking_for'):
                    context['looking_for'] = EmploymentType.objects.filter(id__in=request.POST.getlist('multiselect_id_looking_for'))
                if request.POST.has_key('multiselect_id_industries_of_interest'):
                    context['industries_of_interest'] = Industry.objects.filter(id__in=request.POST.getlist('multiselect_id_industries_of_interest'))
                if request.POST.has_key('multiselect_id_previous_employers'):
                    context['previous_employers'] = Employer.objects.filter(id__in=request.POST.getlist('multiselect_id_previous_employers'))
                if request.POST.has_key('multiselect_id_campus_involvement'):
                    context['campus_involvement'] = CampusOrg.objects.filter(id__in=request.POST.getlist('multiselect_id_campus_involvement'))
                if request.POST.has_key('multiselect_id_languages'):
                    context['languages'] = Language.objects.filter(id__in=request.POST.getlist('multiselect_id_languages'))
                if request.POST.has_key('multiselect_id_countries_of_citizenship'):
                    context['countries_of_citizenship'] = Country.objects.filter(iso__in=request.POST.getlist('multiselect_id_countries_of_citizenship'))
                                    
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
        else:
            return HttpResponseForbidden("Request must be a POST.") 
    else:
        return HttpResponseForbidden("You must be logged in.")     

@login_required
@require_http_methods(["POST"])
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_update_resume(request, form_class=StudentUpdateResumeForm):
    form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
    if form.is_valid():
        form.save()
        resume_status = process_resume(request.user.student)
        errors = {}
        if resume_status == RESUME_PROBLEMS.HACKED:
            data = {'valid':False}
            errors['id_resume'] = messages.resume_problem
            data['errors'] = errors
        elif resume_status == RESUME_PROBLEMS.UNPARSABLE:
            data = {'valid':False}
            data['unparsable_resume'] = True
        else:
            data = {'valid':True}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required
@require_http_methods(["GET"])
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_update_resume_info(request):
    num = len(filter(None, request.user.student.keywords.split(" ")))
    data = {'num_of_extracted_keywords' : num}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@render_to("student_create_campus_org.html")
def student_create_campus_org(request, form_class=CreateCampusOrganizationForm, extra_context=None):
    if request.user.is_authenticated() and hasattr(request.user, "student"):
        if request.method == 'POST':
            form = form_class(data=request.POST)
            if form.is_valid():
                new_campus_org = form.save()
                recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                subject = "New Campus Org: %s" % (new_campus_org) 
                body = render_to_string('student_new_campus_org_email_body.txt', \
                                        {'first_name':request.user.student.first_name, \
                                        'last_name':request.user.student.last_name, \
                                        'email':request.user.email, \
                                        'new_campus_org':new_campus_org})
                message = EmailMessage(subject, body, s.DEFAULT_FROM_EMAIL, recipients)
                message.send()
                data = {"valid":True,
                        "type": new_campus_org.type.name,
                        "name": new_campus_org.name,
                        "id": new_campus_org.id}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                data = {'valid':False, 'errors': form.errors }
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            form = form_class()
        context =  {'form': form }
        context.update(extra_context or {}) 
        return context
    else:
        return HttpResponseForbidden("You must be logged in.")        


@render_to("student_create_language.html")
def student_create_language(request, form_class=CreateLanguageForm, extra_context=None):
    if request.user.is_authenticated() and hasattr(request.user, "student"):
        if request.method == 'POST':
            form = form_class(data=request.POST)
            if form.is_valid():
                new_language_name = form.cleaned_data['name']
                basic = Language.objects.create(name_and_level=new_language_name + " (Basic)", name=new_language_name)
                proficient = Language.objects.create(name_and_level=new_language_name + " (Proficient)", name=new_language_name)
                fluent = Language.objects.create(name_and_level=new_language_name + " (Fluent)", name=new_language_name)
                recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                subject = "New Language: %s" % (new_language_name) 
                body = render_to_string('student_new_language_email_body.txt', \
                                        {'first_name':request.user.student.first_name, \
                                        'last_name':request.user.student.last_name, \
                                        'email':request.user.email, \
                                        'new_language':new_language_name})
                message = EmailMessage(subject, body, s.DEFAULT_FROM_EMAIL, recipients)
                message.send()
                data = {"valid":True, 
                        "name":new_language_name, 
                        "fluent_id":fluent.id, 
                        "proficient_id":proficient.id, 
                        "basic_id":basic.id}  
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                data = {'valid':False}
                data['errors'] = form.errors
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            form = form_class()
            
        context =  { 'form': form }
        context.update(extra_context or {})
        return context
    else:
        return HttpResponseForbidden("You must be logged in.")

@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_resume(request):
    # Show the student his/her resume
    resume = request.user.student.resume.read()
    response = HttpResponse(resume, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s_%s.pdf' % (request.user.last_name.lower(), request.user.first_name.lower())
    return response