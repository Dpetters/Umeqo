"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
import subprocess
import re
import os
import datetime
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.shortcuts import redirect

from events.models import Event
from student import utils
from student.forms import StudentUpdateResumeForm, StudentEmployerSubscriptionsForm
from student.models import Student
from registration.backend import RegistrationBackend
from registration.forms import RegistrationForm
from core.decorators import is_student
from core.forms import CreateCampusOrganizationForm, CreateLanguageForm
from core.models import Language


def student_registration(request,
             backend = RegistrationBackend(), 
             success_url="/student/registeration/complete/", 
             form_class=RegistrationForm,
             disallowed_url='student_registration_disallowed',
             template_name='student_registration.html'):
    
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
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
            
            return HttpResponse(simplejson.dumps(success_url), mimetype="application/json")
    else:
        form = form_class()

    context = {
            'form':form,
            }
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))

# Allows students to create campus organizations that are not listed yet.
@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_create_campus_organization(request, form_class=CreateCampusOrganizationForm): #@UnusedVariable
    
    if request.method == 'POST':
        create_campus_organization_form = form_class(data=request.POST)
        if create_campus_organization_form.is_valid():
            new_campus_organization = create_campus_organization_form.save()
            return HttpResponse(simplejson.dumps({"valid":True, "type":new_campus_organization.type.name, "name":new_campus_organization.name, "id":new_campus_organization.id}))
        return HttpResponse(simplejson.dumps({"valid":False, "error":create_campus_organization_form.errors}))
    else:
        create_campus_organization_form = form_class()
        
    data =  {
            'create_campus_organization_form': create_campus_organization_form
            }
    
    return render_to_response("student_create_campus_organization.html", data, context_instance=RequestContext(request))


# Allows students to create languages that are not listed yet.
@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_create_language(request, form_class=CreateLanguageForm):

    if request.method == 'POST':
        create_language_form = form_class(data=request.POST)
        if create_language_form.is_valid():
            new_language_name = create_language_form.cleaned_data['name']
            basic = Language.objects.create(name=new_language_name + " (Basic)")
            proficient = Language.objects.create(name=new_language_name + " (Proficient)")
            fluent = Language.objects.create(name=new_language_name + " (Fluent)")            
            return HttpResponse(simplejson.dumps({"valid":True, "name":new_language_name, "fluent_id":fluent.id, "proficient_id":proficient.id, "basic_id":basic.id}))
        return HttpResponse(simplejson.dumps({"valid":False, "error":create_language_form.errors}))
    else:
        create_language_form = form_class()
        
    data =  {
            'create_language_form': create_language_form
            }
    
    return render_to_response("student_create_language.html", data, context_instance=RequestContext(request))


# Displays information about the profile creation process to the student. This is where
# we show them why filling out more fields is better.
@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_profile_form_info(request): #@UnusedVariable
    return render_to_response("student_profile_form_info.html")


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_suggested_employers_list(request):
    data={
          'suggested_employers':compute_suggested_employers_list(request.student, request.POST.getlist('already_selected[]'))
          }
    return render_to_response("student_suggested_employers_list.html", data, context_instance=RequestContext(request))


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
    
     
@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_employer_subscriptions(  request,
                                    template_name = "student_employer_subscriptions_dialog.html",
                                    form_class=StudentEmployerSubscriptionsForm,
                                    ):
    student = Student.objects.get(user__exact = request.user)
    
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({"valid":True}))
        return HttpResponse(simplejson.dumps({"valid":False}))
    else:
        form = form_class(instance=student)
        
    data = {
            'form':form,
            }
    
    return render_to_response(template_name, data, context_instance=RequestContext(request))


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_events(request, template_name="student_events.html"):

    try:
        student = request.user.get_profile()
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/student/create/')

    data = {
            'upcoming_events':Event.objects.filter(datetime__gt=datetime.datetime.now()),
            'past_events':Event.objects.filter(datetime__lte=datetime.datetime.now()),
            'user': student,
            }   
    return render_to_response(template_name, data, context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_create_profile(request, form_class=None,
                   template_name='student_create_profile.html',
                   extra_context=None):

    if request.student.profile_created:
        return redirect('student_edit_profile')

    if form_class is None:
        form_class = utils.get_profile_form()
        
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.last_updated = datetime.datetime.now()
            student.profile_created = True
            student.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return process_resume(student)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'form': form,
                               'main_block_header_title':"yes"},
                              context_instance=context)


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_edit_profile(request, form_class=None, success_url=None,
                 template_name='student_edit_profile.html',
                 extra_context=None):

    try:
        profile_obj = request.user.get_profile()
    except ObjectDoesNotExist:
        return redirect('student_create_profile')
    
    
    if success_url is None:
        success_url = reverse('student_home',
                              kwargs={ 'username': request.user.username })
    if form_class is None:
        form_class = utils.get_profile_form()
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
        prev_resume = str(profile_obj.resume)
        if form.is_valid():
            profile = form.save()
            if profile.sat_m != None and profile.sat_v != None and profile.sat_w != None:
                profile.sat_t = profile.sat_m + profile.sat_v + profile.sat_w
                profile.last_updated = datetime.datetime.now()
                profile.save()
            if request.FILES.has_key('resume'):
                subprocess.Popen("rm "+ settings.MEDIA_ROOT + prev_resume, shell=True)
                return process_resume(profile_obj)
            else:
                return HttpResponseRedirect('/student/%s' % request.user + "/")
    else:
        form = form_class(instance=profile_obj)
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              { 'form': form,
                                'profile': profile_obj, },
                              context_instance=context)


@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_home(request, 
                 username,
                 template_name='student_home.html',
                 extra_context=None):

    if username == str(request.user):
        context = {}
        context.update(extra_context or {}) 
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/student/" + str(request.user) + "/")
    

def student_update_resume(request,
                          form_class=StudentUpdateResumeForm):
    print request.is_ajax()
    if request.method == 'POST':
        if request.GET.has_key('base64'):
            pass # NEED TO SUPPORT CHROME LATER
        else:
            form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
            prev_resume =str(request.user.student.resume)
            if form.is_valid():
                subprocess.Popen("rm "+ settings.MEDIA_ROOT + prev_resume, shell=True)
                form.save()
                return process_resume(request.user.student)
    return HttpResponseRedirect('/')

def process_resume(profile):
    
    # Create the resume text directory if it doesn't exist
    resume_text_directory = settings.MEDIA_ROOT + "/resumedata/submitted_resumes/"
    if not os.path.exists(resume_text_directory):
        os.makedirs(resume_text_directory)
        
    # Create the resume directory if it doesn't exist
    resume_directory = settings.MEDIA_ROOT + "/submitted_resumes/"
    if not os.path.exists(resume_directory):
        os.makedirs(resume_directory)
    
    # Convert resume to text
    p = subprocess.Popen("pdftotext " + settings.MEDIA_ROOT + profile.resume.name + " " + settings.MEDIA_ROOT + "resumedata/" + profile.resume.name[:-4] + ".txt", shell=True)
    p.wait()
    
    # Words that we want to parse out of the resume keywords
    stopWords = set(open(settings.ROOT + "/student/stop_words/common.txt").read().split(os.linesep))
    
    # Read in the resume text
    f = open(str(settings.MEDIA_ROOT + "/resumedata/" + profile.resume.name[:-4] + ".txt"))
    allText = f.read()
    f.close()
    
    # Delete the text file
    current_resume_text_file = settings.MEDIA_ROOT + "/resumedata/" + profile.resume.name[:-4] + ".txt"
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
    profile.keywords = result
    profile.last_update = datetime.datetime.now()
    profile.save()
    
    return HttpResponseRedirect('/student/%s' % profile.user + "/")

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def student_invitations(request,
                        template_name="student_invitations.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))