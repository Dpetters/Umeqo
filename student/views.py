"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
import os, datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse

from student.forms import StudentPreferencesForm, StudentRegistrationForm, StudentUpdateResumeForm, StudentEmployerSubscriptionsForm, StudentEditProfileForm, StudentCreateProfileForm
from student.models import Student
from student.view_helpers import process_resume
from registration.forms import PasswordChangeForm
from registration.backend import RegistrationBackend
from core.decorators import is_student
from core.forms import CreateCampusOrganizationForm, CreateLanguageForm
from core.models import Language
from core import messages


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_account_settings(request, template_name="student_account_settings.html",
                             preferences_form_class = StudentPreferencesForm, 
                             change_password_form_class = PasswordChangeForm, extra_context=None):
    
    if request.method == "GET":
        context = {}
        context['preferences_form'] = preferences_form_class(instance = request.user.student.preferences)
        context['change_password_form'] = change_password_form_class(request.user)
        context['last_password_change_date'] = request.user.userattributes.last_password_change_date
        context.update(extra_context or {})
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    return HttpResponseForbidden("Request must be a GET")



@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_preferences(request, preferences_form_class = StudentPreferencesForm, extra_context = None):
    if request.is_ajax():
        if request.method == "POST":
            form = preferences_form_class(data = request.data, instance = request.user.student.studentpreferences)
            if form.is_valid():
                student_preferences = form.save()
                if hasattr(student_preferences, 'save_m2m'):
                    student_preferences.save_m2m()
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
def student_create_profile(request,
                           form_class=StudentCreateProfileForm,
                           template_name='student_create_profile.html',
                           extra_context=None):

    if request.user.student.profile_created:
        if request.is_ajax():
            data = {'valid':True,
                    'success_url':reverse("student_edit_profile")}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        return redirect('student_edit_profile')
        
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
        if form.is_valid():
            student = form.save(commit=False)
            if form.cleaned_data['sat_w'] != None and form.cleaned_data['sat_m'] != None and form.cleaned_data['sat_v'] != None:
                student.sat_t = form.cleaned_data['sat_w'] + form.cleaned_data['sat_v'] + form.cleaned_data['sat_m']
            student.last_updated = datetime.datetime.now()
            student.profile_created = True
            student.save()
            if hasattr(student, 'save_m2m'):
                student.save_m2m()
            return process_resume(student, request.is_ajax())
        else:
            if request.is_ajax():
                data = {'valid': False,
                        'form_errors': form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class()
    
    context = {
               'resume_must_be_a_pdf_message': messages.resume_must_be_a_pdf,
               'form': form
               }

    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_edit_profile(request,
                         form_class=StudentEditProfileForm,
                         template_name='student_edit_profile.html',
                         extra_context=None):

    if not request.user.student.profile_created:
        if request.is_ajax():
            data = {'valid':True,
                    'success_url':reverse("student_create_profile")}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        return redirect('student_create_profile')
        
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
        old_resume_name = str(request.user.student.resume)
        if form.is_valid():
            student = form.save()
            if form.cleaned_data['sat_w'] != None and form.cleaned_data['sat_m'] != None and form.cleaned_data['sat_v'] != None:
                student.sat_t = form.cleaned_data['sat_w'] + form.cleaned_data['sat_v'] + form.cleaned_data['sat_m']
            student.last_updated = datetime.datetime.now()
            student.save()
            if request.FILES.has_key('resume'):
                if os.path.exists(settings.MEDIA_ROOT + old_resume_name):
                    os.remove(settings.MEDIA_ROOT + old_resume_name)
                return process_resume(request.user.student, request.is_ajax())
            else:
                if request.is_ajax():
                    data = {'valid':False,
                            'success_url':reverse("home")}
                    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
                return redirect(reverse('home') + '?msg=profile_saved')
        else:
            if request.is_ajax():
                data = {'valid':False,
                        'form_errors':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class(instance=request.user.student)

    context = {
               'resume_must_be_a_pdf_message' : messages.resume_must_be_a_pdf,
               'form' : form
               }
      
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

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

    
@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_create_campus_organization(request,
                                       form_class=CreateCampusOrganizationForm,
                                       template_name="student_create_campus_organization.html",
                                       extra_context=None):

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
            # Should be caught by javascript. Bug!
            invalid_data = {"valid": False, 
                            "errors": form.errors}
            return HttpResponse(simplejson.dumps(invalid_data), mimetype="application/json")
        else:
            create_campus_organization_form = form_class()
            
        context =  {
                'create_campus_organization_form': create_campus_organization_form
                }
        context.update(extra_context or {}) 
        return render_to_response(template_name,
                                  context,
                                  context_instance=RequestContext(request))
    redirect('home')


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_create_language(request, 
                            form_class=CreateLanguageForm,
                            template_name="student_create_language.html",
                            extra_context=None):
    
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
            # Should be caught by javascript. Bug!
            invalid_data = {"valid": False, 
                            "errors": form.errors}
            return HttpResponse(simplejson.dumps(invalid_data), mimetype="application/json")
        else:
            create_language_form = form_class()
            
        context =  {
                'create_language_form': create_language_form
                }
        context.update(extra_context or {})
        return render_to_response(template_name, 
                                  context, 
                                  context_instance=RequestContext(request))
    redirect('home')


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
        return redirect('student_edit_profile')
    
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
