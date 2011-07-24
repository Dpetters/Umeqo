import os, datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse

from student.forms import StudentPreferencesForm, StudentRegistrationForm, StudentUpdateResumeForm, StudentEmployerSubscriptionsForm, StudentProfilePreviewForm, StudentProfileForm
from student.models import Student
from student.view_helpers import process_resume
from registration.forms import PasswordChangeForm
from registration.backend import RegistrationBackend
from core.decorators import is_student, render_to
from core.forms import CreateCampusOrganizationForm, CreateLanguageForm
from core.models import Language, EmploymentType, Industry, CampusOrg
from core import messages
from employer.models import Employer
from student.enums import RESUME_PROBLEMS
from countries.models import Country


@render_to("student_account_settings.html")
@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_account_settings(request, preferences_form_class = StudentPreferencesForm, 
                             change_password_form_class = PasswordChangeForm, extra_context=None):
    if request.method == "GET":
        context = {}
        page_messages = {
            'password-changed': messages.password_changed,
        }
        msg = request.GET.get('msg', None)
        if msg:
            context["msg"] = page_messages[msg]
        context['preferences_form'] = preferences_form_class(instance = request.user.student.studentpreferences)
        context['change_password_form'] = change_password_form_class(request.user)
        context.update(extra_context or {})
        return context
    return HttpResponseForbidden("Request must be a GET")


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_deactivate_account(request):
    if request.method == "POST":
        pass
    else:
        pass
    

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_preferences(request, preferences_form_class = StudentPreferencesForm, extra_context = None):
    if request.is_ajax():
        if request.method == "POST":
            form = preferences_form_class(data = request.data, instance = request.user.student.studentpreferences)
            if form.is_valid():
                request.user.student.student_preferences = form.save()
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


def student_registration(request,
                         backend = RegistrationBackend(), 
                         template_name = 'student_registration.html',
                         extra_context = None):
    
    success_url = 'student_registration_complete'
    disallowed_url = 'student_registration_disallowed'
    
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    
    if request.method == 'POST':
        form = StudentRegistrationForm(data=request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email']
            new_user = backend.register(request, **form.cleaned_data)
            student = Student(user=new_user)
            student.save()
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
                data = {'valid':False,
                        'form_errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = StudentRegistrationForm()

    context = {
            'form':form,
            'email_already_registered_message': messages.email_already_registered,
            'passwords_dont_match_message': messages.passwords_dont_match
            }
    
    context.update(extra_context or {}) 
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


def student_registration_complete(request,
            template_name='student_registration_complete.html',
            extra_context = None):
    email = request.GET.get('email', None)
    context = {'email': email}
    context.update(extra_context)
    return render_to_response(template_name, context,
            context_instance = RequestContext(request))
    

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
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
            student.last_updated = datetime.datetime.now()
            student.profile_created = True
            student.save()
            resume_status = None
            data = {'valid':True} 
            if request.FILES.has_key('resume'):
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
            data = {'valid':False}
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.auto_id] = field.errors[0]
            if form.non_field_errors():
                errors['non_field_error'] = form.non_field_errors()[0]
            data['errors'] = errors
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    else:
        if request.is_ajax():
            return HttpResponseForbidden("GET request cannot be ajax.") 
        else:
            form = form_class(instance=request.user.student)
            context = { 'form' : form,
                        'edit' : request.user.student.profile_created }
              
            context.update(extra_context or {})
            return context


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
@render_to("student_profile_preview.html")
def student_profile_preview(request,
                            form_class=StudentProfilePreviewForm,
                            extra_context=None):

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
                       'comment':messages.student_profile_preview_comment,
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
            print form.errors
            if form.non_field_errors():
                error_html = form.non_field_errors()[0]
            else:
                for field in form:
                    if field.errors:
                        error_html = field.errors[0]
                        break
            return HttpResponse("<div class='message_section'>%s</div>" % error_html)
    else:
        return HttpResponseForbidden("Request must be a GET.") 

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_update_resume(request,
                          form_class=StudentUpdateResumeForm):
    
    if request.is_ajax() and request.method == 'POST':
        form = form_class(data=request.POST,
                          files=request.FILES,
                          instance=request.user.student)
        old_resume_name = str(request.user.student.resume)
        if form.is_valid():
            os.remove(settings.MEDIA_ROOT + old_resume_name)
            form.save()
            return process_resume(request.user.student, request.is_ajax())
    return redirect('home')

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_update_resume_info(request):
    
    if request.is_ajax():
        data = {'path_to_new_resume' : str(request.user.student.resume), 
                'num_of_extracted_keywords' : str(len(request.user.student.keywords.split(" ")))}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    return redirect('home')

"""
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_preferences(request, preferences_form_class = StudentPreferencesForm, extra_context = None):
    if request.is_ajax():
        if request.method == "POST":
            form = preferences_form_class(data = request.data, instance = request.user.student.studentpreferences)
            if form.is_valid():
                request.user.student.student_preferences = form.save()
                if hasattr(student_preferences, 'save_m2m'):
                    request.user.student.student_preferences.save_m2m()
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
"""
@render_to("student_create_campus_organization.html")
def student_create_campus_organization(request, form_class=CreateCampusOrganizationForm, extra_context=None):
    if request.user.is_authenticated() and hasattr(request.user, "student"):
        if request.is_ajax():
            if request.method == 'POST':
                form = form_class(data=request.POST)
                if form.is_valid():
                    new_campus_organization = form.save()
                    data = {"valid":True,
                            "type": new_campus_organization.type.name,
                            "name": new_campus_organization.name,
                            "id": new_campus_organization.id}
                    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
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
                form = form_class()
            context =  {'form': form }
            context.update(extra_context or {}) 
            return context
        else:
            return HttpResponseForbidden("Request must be a valid XMLHttpRequest")
    else:
        return HttpResponseForbidden("You must be logged in.")        


@render_to()
def student_create_language(request, form_class=CreateLanguageForm, extra_context=None):
    
    if request.user.is_authenticated() and hasattr(request.user, "student"):
        if request.is_ajax():
            if request.method == 'POST':
                form = form_class(data=request.POST)
                if form.is_valid():
                    new_language_name = form.cleaned_data['name']
                    basic = Language.objects.create(name=new_language_name + " (Basic)")
                    proficient = Language.objects.create(name=new_language_name + " (Proficient)")
                    fluent = Language.objects.create(name=new_language_name + " (Fluent)")
                    data = {"valid":True, 
                            "name":new_language_name, 
                            "fluent_id":fluent.id, 
                            "proficient_id":proficient.id, 
                            "basic_id":basic.id}  
                    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
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
                create_language_form = form_class()
                
            context =  { 'create_language_form': create_language_form,
                        'TEMPLATE': "student_create_language.html" }
            context.update(extra_context or {})
            return context
        else:
            return HttpResponseForbidden("Request must be a valid XMLHttpRequest")
    else:
        return HttpResponseForbidden("You must be logged in.")     


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_employer_subscriptions(request,
                                   template_name = "student_employer_subscriptions_dialog.html",
                                   form_class=StudentEmployerSubscriptionsForm,
                                   extra_context = None):
    
    if request.method == 'POST':
        form = form_class(data=request.POST, 
                          files=request.FILES, 
                          instance=request.user.student)
        if form.is_valid():
            form.save()
            data = {"valid":True}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        invalid_data = {"valid":False,
                        "error":form.errors}
        return HttpResponse(simplejson.dumps(invalid_data), mimetype="application/json")
    else:
        form = form_class(instance=request.user.student)
        
    context = {
               'student_employer_subscriptions_form': form
               }
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_invitations(request,
                        template_name="student_invitations.html",
                        extra_context=None):

    if request.user.student.profile_created:
        return redirect('student_profile')
    
    context = {}
    context.update(extra_context or {})  
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_resume(request):
    # Show the student his/her resume
    resume = request.user.student.resume.read()
    response = HttpResponse(resume, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s_%s.pdf' % (request.user.last_name.lower(), request.user.first_name.lower())
    return response
"""
def compute_suggested_employers_list(student, exclude = None):
    suggested_employers = []
    if exclude:
        for industry in student.industries_of_interest.all():
            for employer in industry.employer_set.all().exclude(id__in=[o.id for o in student.subscribed_employers.all()]).exclude(company_name__in=[n for n in exclude]):
                suggested_employers.append(employer.name)
    
        for employer in student.previous_employers.all():
            for industry in employer.industry.all():
                for employer in industry.employer_set.all().exclude(    name__in=[o for o in suggested_employers]).exclude(    name__in=[n for n in exclude]):
                    suggested_employers.append(employer.name)
    else:
        for industry in student.industries_of_interest.all():
            for employer in industry.employer_set.all().exclude(id__in=[o.id for o in student.subscribed_employers.all()]):
                suggested_employers.append(employer.name)
    
        for employer in student.previous_employers.all():
            for industry in employer.industry.all():
                for employer in industry.employer_set.all().exclude(    name__in=[o for o in suggested_employers]):
                    suggested_employers.append(employer.name)
    
    random.shuffle(suggested_employers)

    if len(suggested_employers) > 5:
        suggested_employers = suggested_employers[:6]
    elif len(suggested_employers) > 4:
        suggested_employers = suggested_employers[:5]
    elif len(suggested_employers) > 3:
        suggested_employers = suggested_employers[:4]
    elif len(suggested_employers) > 2:
        suggested_employers = suggested_employers[:3]
    elif len(suggested_employers) > 1:
        suggested_employers = suggested_employers[:2]
    elif len(suggested_employers) > 0:
        suggested_employers = suggested_employers[:1]
        
    return suggested_employers
"""
