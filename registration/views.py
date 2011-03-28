"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import ldap, datetime #@UnusedImport
from django.conf import settings

from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.views.decorators.cache import never_cache

from registration.view_helpers import modify_redirect
from registration.forms import RegistrationForm
from events.models import Event
from employer.models import Employer
from registration.backends import get_backend
from core.decorators import is_student

def activate(request, backend,
             template_name='registration/invalid_activation_link.html',
             success_url=None, 
             extra_context=None, 
             **kwargs):

    backend = get_backend(backend)
    account = backend.activate(request, **kwargs)

    if account:
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)


def register(request,
             backend, 
             success_url="/student/register/complete/", 
             form_class=RegistrationForm,
             disallowed_url='registration_disallowed',
             template_name='registration/student_registration.html',
             extra_context=None):

    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            
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
            
            form.cleaned_data['username']= username
            new_user = backend.register(request, **form.cleaned_data)
            
            # A safety just in case - if for whatever reason the student group has not been created at this point,
            # it should not prevent the user form registering. Therefore we create the group for them.
            try:
                student_group = Group.objects.get(name=settings.STUDENT_GROUP_NAME)
            except Group.DoesNotExist:
                Group.objects.create(name=settings.STUDENT_GROUP_NAME)
            new_user.groups.add(student_group)
            return HttpResponse(simplejson.dumps(success_url), mimetype="application/json")
    else:
        form = form_class()
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    data = {
            'form':form,
            }
    return render_to_response(template_name,
                              data,
                              context_instance=context)
    
@never_cache
def home(request, 
          template_name='homepage.html'):
    
    request.session.set_test_cookie()

    if not request.user.is_anonymous():
        try:
            Employer.objects.get(user=request.user)
            url = "/employer/"
        except Employer.DoesNotExist:
            url = "/student/"
        return  HttpResponseRedirect(url + str(request.user) + "/")
    
    action = request.REQUEST.get('action', '')

    data ={
        'action':action
    }
    
    kwargs = {}
    kwargs['datetime__gt'] = datetime.datetime.now()
    events = Event.objects.filter(**kwargs).order_by("-datetime_created")
    data['events'] = list(events)[:3]
    
    return render_to_response(template_name, data, context_instance=RequestContext(request))



def login_dialog(request,
                 template_name='registration/login_dialog.html',
                 form_class=AuthenticationForm,
                 redirect_field_name=REDIRECT_FIELD_NAME):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user_cache = authenticate(username = username, password=password)
            if user_cache is None:
                return HttpResponse(simplejson.dumps("invalid"), mimetype="application/json")
            elif not user_cache.is_active:
                return HttpResponse(simplejson.dumps("inactive"), mimetype="application/json")
            else:
                if not request.session.test_cookie_worked():
                    return HttpResponse(simplejson.dumps("cookies_disabled"), mimetype="application/json")
                auth_login(request, user_cache)
                return HttpResponse(simplejson.dumps(modify_redirect(request, redirect_to)), mimetype="application/json")
    else:
        login_form = form_class(request)
        
    data = {
            'login_form':login_form,
            }

    return render_to_response(template_name, data, context_instance=RequestContext(request))



@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def password_change(request, 
                    template_name='registration/password_change_form.html', 
                    post_change_redirect=None, 
                    password_change_form=PasswordChangeForm):
    
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    
    try:
        employer = Employer.objects.get(user=request.user)
        user = employer.company_name
    except Employer.DoesNotExist:
        user = request.user
    
    data = {
            'form': form,
            'user': user,
            }
    
    return render_to_response(template_name, 
                              data, 
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(is_student, login_url=settings.LOGIN_URL)
def password_change_done(request, 
                         template_name='registration/password_change_done.html'):
    try:
        employer = Employer.objects.get(user=request.user)
        user = employer.company_name
    except Employer.DoesNotExist:
        user = request.user
    data={
          'user':user,
          }
    return render_to_response(template_name, 
                              data, 
                              context_instance=RequestContext(request))

def login_redirect(request):
    return HttpResponseRedirect(modify_redirect(request))