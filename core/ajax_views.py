"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.contrib.auth.models import User
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.validators import URLValidator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from core.models import Course, CampusOrg, Language
from student.models import Student
from employer.models import Employer

@login_required
def check_website(request):
    # Only do the check if this is an ajax method
    if request.is_ajax():
        # Create the Validator
        v =  URLValidator(verify_exists = True)
        # Return a false if the website query param is missing
        if request.GET.has_key("website"):
            try:
                website = request.GET.get("website")
                # Add the http if the user forgot to include it
                if website[:5] != "http":
                    website = "http://" + website
                v(website)
                return HttpResponse(simplejson.dumps(True), mimetype="application/json")
            except ValidationError:
                pass
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return HttpResponseRedirect('/')


# Check if a campus organization with the supplied name already exists
@login_required
def check_campus_organization_uniqueness(request):
    # Only do the check if this is an ajax method
    if request.is_ajax():
        # Return a false if the name query param is missing
        if request.GET.has_key("name"):
            try:
                CampusOrg.objects.get(name=request.GET.get("name"))
                return HttpResponse(simplejson.dumps(False), mimetype="application/json")
            except CampusOrg.DoesNotExist:
                pass
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseRedirect('/')

# Check if a language with the supplied name already exists
@login_required
def check_language_uniqueness(request):
    # Only do the check if this is an ajax method
    if request.is_ajax():
        # Return a false if the name query param is missing
        if request.GET.has_key("name"):
            try:
                Language.objects.get(name=request.GET.get("name") + " (Fluent)")
                return HttpResponse(simplejson.dumps(False), mimetype="application/json")
            except Language.DoesNotExist:
                pass
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseRedirect('/')

    
def check_password(request):
    if request.is_ajax():
        old_password = request.GET.get("old_password")
        if request.user.check_password(old_password):
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
        else:
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return HttpResponseRedirect('/')

def check_username_existence(request):
    if request.is_ajax():
        username = request.GET.get("username")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                User.objects.get(email=username)
            except User.DoesNotExist:
                try:
                    Employer.objects.get(company_name = username).user
                except Employer.DoesNotExist:
                    return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseRedirect('/')
 
def check_email_existence(request):
    if request.is_ajax():
        e = request.GET.get("email")
        try:
            User.objects.get(email=e)
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
        except User.DoesNotExist:
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    return HttpResponseRedirect('/')

def check_email_availability(request):
    if request.is_ajax():
        e = request.GET.get("email")
        try:
            User.objects.get(email=e)
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except User.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseRedirect('/')

def get_course_info(request):
    if request.is_ajax():
        get = request.GET.copy()
        if get.has_key('course_name'):
            course_name = get['course_name']
            course = Course.objects.get(name=course_name)
            if course:
                data = {'name': course.name, 'num': course.num, 'admin' : course.admin, 'email':course.email, 'website' :course.website, 'description': course.description, 'image':course.image.name}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                return HttpResponseServerError()
    return HttpResponseRedirect('/')

@login_required
def resume_info(request):
    if request.is_ajax():
        student = Student.objects.get(user=request.user)
        data = {'path_to_new_resume' : str(student.resume), 'num_of_extracted_keywords' : str(len(student.keywords.split(" ")))}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    return HttpResponseRedirect('/')
