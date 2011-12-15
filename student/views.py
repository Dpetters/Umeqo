from __future__ import division
from __future__ import absolute_import

import datetime

from django.conf import settings as s
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.views.decorators.http import require_http_methods, require_POST
from django.utils import simplejson
from django.template.loader import render_to_string

from notification.models import NoticeSetting, NoticeType, EMAIL
from student.forms import StudentAccountDeactivationForm, StudentPreferencesForm, StudentRegistrationForm, StudentUpdateResumeForm,\
                            StudentProfilePreviewForm, StudentProfileForm, BetaStudentRegistrationForm
from student.models import Student, StudentDeactivation, StudentInvite
from student.view_helpers import process_resume
from registration.forms import PasswordChangeForm
from registration.backend import RegistrationBackend
from core.decorators import is_student, render_to, is_recruiter, agreed_to_terms
from core.forms import CreateLanguageForm
from core.email import send_html_mail
from campus_org.forms import CreateCampusOrganizationForm
from core.models import Language, EmploymentType, Industry
from events.models import Attendee
from campus_org.models import CampusOrg
from core import messages
from employer.models import Employer
from student import enums as student_enums
from countries.models import Country


@render_to('student_registration_help.html')
def student_registration_help(request, extra_context=None):
    if request.is_ajax():
        return {}
    else:
        return HttpResponseBadRequest("Request must be ajax.")
    
@login_required
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to('student_profile_unparsable_resume.html')
def student_profile_unparsable_resume(request, extra_context=None):
    if request.is_ajax():
        return {}
    else:
        return HttpResponseBadRequest("Request must be ajax.")

@login_required
@agreed_to_terms
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_account.html")
def student_account(request, preferences_form_class = StudentPreferencesForm, 
                    change_password_form_class = PasswordChangeForm, 
                    extra_context=None):
    
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

@require_POST
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
def student_increment_resume_view_count(request):
    if request.POST.has_key("student_id"):
        student = Student.objects.get(id=request.POST['student_id'])
        student.studentstatistics.resume_view_count += 1
        student.studentstatistics.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Student Id is missing")

@login_required
@agreed_to_terms
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
@agreed_to_terms
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
            if not Student.objects.filter(user=new_user).exists():
                if form.cleaned_data.has_key("first_name") and form.cleaned_data.has_key("last_name"):
                    student = Student(user=new_user, first_name = form.cleaned_data["first_name"], last_name = form.cleaned_data["last_name"])
                else:
                    student = Student(user=new_user)
                umeqo = Employer.objects.get(name="Umeqo")
                student.save()
                if form.cleaned_data.has_key("course"):
                    student.first_major=form.cleaned_data["course"]
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

@render_to('student_registration_complete.html')
def student_registration_complete(request, extra_context = None):
    email = request.GET.get('email', None)
    context = {'email': email}
    context.update(extra_context)
    return context

@login_required
@agreed_to_terms
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_profile.html")
def student_profile(request, form_class=StudentProfileForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
        if form.is_valid():
            print request.POST
            student = form.save()
            if form.cleaned_data['sat_w'] != None and form.cleaned_data['sat_m'] != None and form.cleaned_data['sat_v'] != None:
                student.sat_t = int(form.cleaned_data['sat_w']) + int(form.cleaned_data['sat_v']) + int(form.cleaned_data['sat_m'])
            else:
                student.sat_t = None
            data = {'valid':True, 'unparsable_resume':False}
            if request.FILES.has_key('resume'):
                resume_status = process_resume(request.user.student)
                if resume_status == student_enums.RESUME_PROBLEMS.HACKED:
                    data = {'valid':False}
                    errors = {'resume': messages.resume_problem}
                    data['errors'] = errors
                elif resume_status == student_enums.RESUME_PROBLEMS.UNPARSABLE and request.POST['ingore_unparsable_resume'] == "false":
                    data = {'valid':False}
                    data['unparsable_resume'] = True
            if data['valid'] and not data['unparsable_resume']:
                student.profile_created = True
                student.last_updated = datetime.datetime.now()
                student.save()
                for a in Attendee.objects.filter(email=student.user.email):
                    a.student = student
                    a.save()
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
                    'previous_employers_max':s.SP_MAX_PREVIOUS_EMPLOYERS,
                    'max_industries':s.EP_MAX_INDUSTRIES}
        context.update(extra_context or {})
        return context


@login_required
@agreed_to_terms
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_profile_preview.html")
def student_profile_preview(request, form_class=StudentProfilePreviewForm,
                            extra_context=None):
    if request.user.is_authenticated() and hasattr(request.user, "student"):
        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
            if form.is_valid():
                print request.POST
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
        else:
            return HttpResponseForbidden("Request must be a POST.") 
    else:
        return HttpResponseForbidden("You must be logged in.")     

@login_required
@agreed_to_terms
@require_http_methods(["POST"])
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_update_resume(request, form_class=StudentUpdateResumeForm):
    form = form_class(data=request.POST, files=request.FILES, instance=request.user.student)
    if form.is_valid():
        form.save()
        resume_status = process_resume(request.user.student)
        errors = {}
        if resume_status == student_enums.RESUME_PROBLEMS.HACKED:
            data = {'valid':False}
            errors['id_resume'] = messages.resume_problem
            data['errors'] = errors
        elif resume_status == student_enums.RESUME_PROBLEMS.UNPARSABLE:
            request.user.student.last_updated = datetime.datetime.now()
            request.user.student.save()
            data = {'valid':False}
            data['unparsable_resume'] = True
        else:
            request.user.student.last_updated = datetime.datetime.now()
            request.user.student.save()
            data = {'valid':True}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required
@agreed_to_terms
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
                body = render_to_string('new_campus_org_email_body.html', \
                                        {'first_name':request.user.student.first_name, \
                                        'last_name':request.user.student.last_name, \
                                        'email':request.user.email, \
                                        'new_campus_org':new_campus_org})
                send_html_mail(subject, body, recipients)
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
    else:
        return HttpResponseForbidden("You must be logged in.")

@agreed_to_terms
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
                body = render_to_string('new_language_email_body.html', \
                                        {'first_name':request.user.student.first_name, \
                                        'last_name':request.user.student.last_name, \
                                        'email':request.user.email, \
                                        'new_language':new_language_name})
                send_html_mail(subject, body, recipients)
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
    else:
        return HttpResponseForbidden("You must be logged in.")

@login_required
@agreed_to_terms
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_resume(request):
    # Show the student his/her resume
    resume = request.user.student.resume.read()
    response = HttpResponse(resume, mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s_%s.pdf' % (request.user.last_name.lower(), request.user.first_name.lower())
    return response

@login_required
@user_passes_test(is_recruiter, login_url=s.LOGIN_URL)
def specific_student_resume(request, student_id):
    if request.user.recruiter.employer.subscribed():
        student_query = Student.objects.filter(id=student_id)
        if student_query.exists():
            student = student_query.get()
            resume = student.resume.read()
            response = HttpResponse(resume, mimetype='application/pdf')
            response['Content-Disposition'] = 'inline; filename=%s_%s_%s.pdf' % (student.id, student.user.last_name.lower(), student.user.first_name.lower())
            return response
    raise Http404

"""
@login_required
@agreed_to_terms
@require_GET
@user_passes_test(is_student, login_url=s.LOGIN_URL)
@render_to("student_statistics.html")
def student_statistics(request):
    context = {'student_body_statistics_form': StudentBodyStatisticsForm(),
               'second_major_form':StatisticsSecondMajorForm()}
    return context

@login_required
@agreed_to_terms
@require_GET
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_statistics_second_major(request):
    data = {}
    first_major = Course.objects.get(id=request.GET['first_major'])
    data['title'] = "Second Major Statistics for %s" % first_major.name
    courses = list(Course.objects.all().exclude(name=first_major.name))
    data['categories'] = ['None'] + [c.num for c in courses]
    data['series'] = {'data':[len(Student.objects.filter(first_major = first_major, second_major = None))]}
    for second_major in courses:
        data['series']['data'].append(len(Student.objects.filter(first_major = first_major, second_major = second_major)))
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@login_required
@agreed_to_terms
@require_GET
@user_passes_test(is_student, login_url=s.LOGIN_URL)
def student_body_statistics(request):
    data = {}
    data['title'] = ""
    if request.GET['x_axis'] == student_enums.SCHOOL_YEAR:
        school_years = SchoolYear.objects.all()
        if request.GET['y_axis'] == student_enums.GPA:
            data['name'] = "GPA vs. School Year"
            data['y_axis_text'] = "GPA"
            data['y_axis_min'] = 0
            data['y_axis_max'] = 5
            data['categories'] = []
            data['series'] = {'data':[]}
            for school_year in school_years:
                students = Student.objects.filter(school_year = school_year, profile_created=True)
                if students:
                    data['categories'].append("%s" % school_year.name_plural)
                    num_of_students = 0
                    gpa_sum = 0
                    for s in students:
                        if s.gpa != 0:
                            num_of_students += 1
                            gpa_sum += s.gpa
                    if num_of_students != 0:
                        data['series']['data'].append(float(gpa_sum)/num_of_students)
        elif request.GET['y_axis'] == student_enums.NUM_OF_PREVIOUS_EMPLOYERS:
            data['name'] = "# of Previous Employers vs. School Year"
            data['y_axis_text'] = "# of Previous Employers"
            data['categories'] = []
            data['series'] = {'data':[]}
            for school_year in school_years:
                students = Student.objects.filter(school_year = school_year, profile_created=True)
                if students:
                    data['categories'].append("%s" % school_year.name_plural)
                    data['series']['data'].append(float(sum([len(s.previous_employers.all()) for s in students]))/len(students))
    if request.GET['x_axis'] == student_enums.MAJOR:
        courses = Course.objects.all()
        if request.GET['y_axis'] == student_enums.GPA:
            data['name'] = "GPA vs. Major"
            data['y_axis_text'] = "GPA"
            data['y_axis_min'] = 0
            data['y_axis_max'] = 5
            data['categories'] = []
            data['series'] = {'data':[]}
            for course in courses:
                students = Student.objects.filter(first_major = course, profile_created=True)
                if students:
                    data['categories'].append("%s" % course.num)
                    num_of_students = 0
                    gpa_sum = 0
                    for s in students:
                        if s.gpa != 0:
                            num_of_students += 1
                            gpa_sum += s.gpa
                    if num_of_students != 0:
                        data['series']['data'].append(float(gpa_sum)/num_of_students)
        elif request.GET['y_axis'] == student_enums.NUM_OF_PREVIOUS_EMPLOYERS:
            data['name'] = "# of Previous Employers vs. Major"
            data['y_axis_text'] = "# of Previous Employers"
            data['categories'] = []
            data['series'] = {'data':[]}
            for course in courses:
                students = Student.objects.filter(first_major = course, profile_created=True)
                if students:
                    data['categories'].append("%s" % course.num)
                    data['series']['data'].append(float(sum([len(s.previous_employers.all()) for s in students]))/len(students))
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
"""