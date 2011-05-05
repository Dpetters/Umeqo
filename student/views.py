"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
import subprocess
import re
import os
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse

from events.models import Event
from student.forms import StudentRegistrationForm, StudentUpdateResumeForm, StudentEmployerSubscriptionsForm, StudentEditProfileForm, StudentCreateProfileForm
from student.models import Student
from registration.backend import RegistrationBackend
from core.decorators import is_student
from core.forms import CreateCampusOrganizationForm, CreateLanguageForm
from core.models import Language


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_account_settings(request, 
                             template_name="student_account_settings.html", 
                             extra_context=None):

    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name, 
                              context, 
                              context_instance=RequestContext(request))


def student_registration(request,
             backend = RegistrationBackend(), 
             form_class = StudentRegistrationForm,
             success_url = 'student_registration_complete', 
             disallowed_url = 'student_registration_disallowed',
             template_name = 'student_registration.html',
             extra_context = None):
    
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            """
            ending = email.split("@")[1]
            if ending != "mit.edu":
                return HttpResponse(simplejson.dumps("notmit"), mimetype="application/json")

            con = ldap.open('ldap.mit.edu')
            con.simple_bind_s("", "")
            dn = "dc=mit,dc=edu"
            fields = ['cn', 'sn', 'givenName', 'mail', ]
            result = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+username, fields)
            if result == []:
                return HttpResponse(simplejson.dumps("notstudent"), mimetype="application/json") 
            """
            form.cleaned_data['username']= username
            new_user = backend.register(request, **form.cleaned_data)
            
            Student.objects.create(user=new_user)

            return HttpResponse(simplejson.dumps(reverse(success_url)), mimetype="application/json")
    else:
        form = form_class()

    context = {
            'form':form,
            }
    context.update(extra_context or {}) 
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_create_profile(request,
                           form_class=StudentCreateProfileForm,
                           template_name='student_create_profile.html',
                           extra_context=None):

    if request.user.student.profile_created:
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
            return process_resume(student)
    else:
        form = form_class()
    
    context = {
               'form' : form
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
                return process_resume(request.user.student)
            else:
                return redirect('home')
    else:
        form = form_class(instance=request.user.student)

    context = {
               'form' : form
               }
      
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_resume_info(request):
    
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
                return HttpResponse(simplejson.dumps(data))
            invalid_data = {"valid": False, 
                            "error": form.errors}
            return HttpResponse(simplejson.dumps(invalid_data))
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
                return HttpResponse(simplejson.dumps(data))
            invalid_data = {"valid": False, 
                            "error": form.errors}
            return HttpResponse(simplejson.dumps(invalid_data))
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
            return HttpResponse(simplejson.dumps(data))
        invalid_data = {"valid":False,
                        "error":form.errors}
        return HttpResponse(simplejson.dumps(invalid_data))
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
def student_events(request,
                   template_name = "student_events.html",
                   extra_context = None):

    if request.user.student.profile_created:
        return redirect('student_edit_profile')
    
    context = {
            'upcoming_events': Event.objects.filter(datetime__gt=datetime.datetime.now()),
            'past_events': Event.objects.filter(datetime__lte=datetime.datetime.now()),
            }
    context.update(extra_context or {})
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_event(request,
                        template_name="student_event.html",
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
def student_update_resume(request,
                          form_class=StudentUpdateResumeForm):
    
    if request.is_ajax() and request.method == 'POST':
        if request.GET.has_key('base64'):
            pass # NEED TO SUPPORT CHROME LATER
        else:
            form = form_class(data=request.POST,
                              files=request.FILES,
                              instance=request.user.student)
            old_resume_name =str(request.user.student.resume)
            if form.is_valid():
                os.remove(settings.MEDIA_ROOT + old_resume_name)
                form.save()
                return process_resume(request.user.student)
    return redirect('home')


def process_resume(student):
    
    # Create the resume text directory if it doesn't exist
    resume_text_directory = settings.MEDIA_ROOT + "/resumedata/submitted_resumes/"
    if not os.path.exists(resume_text_directory):
        os.makedirs(resume_text_directory)
        
    # Create the resume directory if it doesn't exist
    resume_directory = settings.MEDIA_ROOT + "/submitted_resumes/"
    if not os.path.exists(resume_directory):
        os.makedirs(resume_directory)
    
    # Convert resume to text
    p = subprocess.Popen("pdftotext " + settings.MEDIA_ROOT + student.resume.name + " " + settings.MEDIA_ROOT + "resumedata/" + student.resume.name[:-4] + ".txt", shell=True)
    p.wait()
    
    # Words that we want to parse out of the resume keywords
    stopWords = set(open(settings.ROOT + "/student/stop_words/common.txt").read().split(os.linesep))
    
    # Read in the resume text
    f = open(str(settings.MEDIA_ROOT + "/resumedata/" + student.resume.name[:-4] + ".txt"))
    allText = f.read()
    f.close()
    
    # Delete the text file
    current_resume_text_file = settings.MEDIA_ROOT + "/resumedata/" + student.resume.name[:-4] + ".txt"
    if os.path.exists(current_resume_text_file):
        os.remove(current_resume_text_file)
    
    # Get rid of stop words
    fullWords = re.findall(r'[a-zA-Z]{3,}', allText)
    result=""
    for word in fullWords:
        word=word.lower()
        if word not in stopWords:
            result += " " + word
    
    # Update the student profile and save
    student.keywords = result
    student.last_update = datetime.datetime.now()
    student.save()
    
    return redirect('home')

"""
def compute_suggested_employers_list(student, exclude = None):
    suggested_employers = []
    if exclude:
        for industry in student.industries_of_interest.all():
            for employer in industry.employer_set.all().exclude(id__in=[o.id for o in student.subscribed_employers.all()]).exclude(company_name__in=[n for n in exclude]):
                suggested_employers.append(employer.company_name)
    
        for employer in student.previous_employers.all():
            for industry in employer.industry.all():
                for employer in industry.employer_set.all().exclude(company_name__in=[o for o in suggested_employers]).exclude(company_name__in=[n for n in exclude]):
                    suggested_employers.append(employer.company_name)
    else:
        for industry in student.industries_of_interest.all():
            for employer in industry.employer_set.all().exclude(id__in=[o.id for o in student.subscribed_employers.all()]):
                suggested_employers.append(employer.company_name)
    
        for employer in student.previous_employers.all():
            for industry in employer.industry.all():
                for employer in industry.employer_set.all().exclude(company_name__in=[o for o in suggested_employers]):
                    suggested_employers.append(employer.company_name)
    
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