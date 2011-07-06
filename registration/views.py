"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
from datetime import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.views import logout as auth_logout_then_login
from django.contrib.sessions.models import Session
from django.conf import settings

from registration.forms import PasswordChangeForm
from registration.backend import RegistrationBackend
from registration.models import SessionKey
from registration.view_helpers import modify_redirect
from core import messages


def login(request,
          redirect_field_name = REDIRECT_FIELD_NAME,
          template_name='homepage.html'):

    if request.is_ajax():
        if request.method == "POST":
            redirect_to = request.POST.get(redirect_field_name, '')
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user = authenticate(username = username, password=password)
                if user is None:
                    return HttpResponse(simplejson.dumps({"valid":False, "error":_(messages.incorrect_username_password_combo)}), mimetype="application/json")
                elif not user.is_active:
                    return HttpResponse(simplejson.dumps({"valid":False, "error":_(messages.account_suspended)}), mimetype="application/json")
                else:
                    if not request.session.test_cookie_worked():
                        return HttpResponse(simplejson.dumps({"valid":False, "error":_(messages.enable_cookies)}), mimetype="application/json")
                    print "Before: " + request.session.session_key
                    auth_login(request, user)
                    print "After: " + request.session.session_key
                    SessionKey.objects.create(user=user, session_key=request.session.session_key)
                    return HttpResponse(simplejson.dumps({"valid":True, "success_url":modify_redirect(request, redirect_to)}), mimetype="application/json")
    return redirect("home")


@login_required
def logout(request, login_url=None, current_app=None, extra_context=None):
    SessionKey.objects.filter(session_key = request.session.session_key).delete()
    return auth_logout_then_login(request, login_url, current_app, extra_context)

@login_required
def deactivate_account(request):
    if request.method == "POST":
        pass
    else:
        pass
        SessionKey.objects.filter(session_key = request.session.session_key).delete()

@login_required
def password_change(request,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    
    if request.is_ajax():
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.userattributes.last_password_change_date = datetime.now()
            for session_key_object in request.user.sessionkey_set.all():
                Session.objects.get(session_key=session_key_object.session_key).delete()
            request.user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, request.user)
            data = {'valid':True}
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
        return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


def activate_user(request, 
                  backend = RegistrationBackend(),
                  template_name='invalid_activation_link.html',
                  success_url=None, 
                  extra_context=None, 
                  **kwargs):

    user = backend.activate(request, **kwargs)
    if user:
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        auth_login(request, user)
        SessionKey.objects.create(user=user, session_key=request.session.session_key)
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, user)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)
        
    kwargs.update(extra_context or {})
    return render_to_response(template_name,
                              kwargs,
                              context_instance=RequestContext(request))
