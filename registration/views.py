from datetime import datetime

from django.conf import settings
from django.contrib.auth import  login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as auth_logout_then_login
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson

from registration.backend import RegistrationBackend
from registration.forms import PasswordChangeForm


@login_required
def logout(request, login_url=None, current_app=None, extra_context=None):
    return auth_logout_then_login(request, login_url, current_app, extra_context)

@login_required
def deactivate_account(request):
    if request.method == "POST":
        pass
    else:
        pass

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
            request.user.sessionkey_set.all().delete()
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
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, user)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)
        
    kwargs.update(extra_context or {})
    return render_to_response(template_name,
                              kwargs,
                              context_instance=RequestContext(request))
