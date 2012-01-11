from datetime import datetime, timedelta
import urllib
import urllib2

from django.conf import settings as s
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth.views import logout as auth_logout_then_login_view, login as auth_login_view
from django.contrib.sessions.models import Session
from django.contrib.sites.models import get_current_site
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils import simplejson

from campus_org.models import CampusOrg
from core.decorators import render_to, is_superuser, is_student, is_campus_org, is_recruiter
from core.forms import EmailAuthenticationForm as AuthenticationForm, SuperLoginForm
from core.view_helpers import get_ip
from core.signals import us_user_logged_in
from registration.models import LoginAttempt
from registration.backend import RegistrationBackend
from registration.forms import PasswordChangeForm

def logout(request, login_url=None, current_app=None, extra_context=None):
    return auth_logout_then_login_view(request, login_url, current_app, extra_context)

@render_to('login.html')
def login(request, template_name="login.html", authentication_form=AuthenticationForm, login_url=None, current_app=None, extra_context={}):
    if request.user.is_superuser:
        return redirect(reverse('super_login'))
    elif request.user.is_authenticated():
        return redirect(reverse('home'))

    # Log the login attempt.
    ip_address = get_ip(request)
    if ip_address:
        LoginAttempt.objects.create(ip_address=ip_address)
    
    half_day_ago = datetime.now() - timedelta(hours=12)
    login_attempts = LoginAttempt.objects.all().filter(ip_address=ip_address).filter(attempt_datetime__gt=half_day_ago).count()

    extra_context.update({
        'show_captcha': (login_attempts >= 10),
        'invalid_captcha': False,
        'RECAPTCHA_PUBLIC_KEY': s.RECAPTCHA_PUBLIC_KEY,
    })
    if request.method == 'POST' and login_attempts > 10:
        captcha_params = urllib.urlencode({
            'privatekey': s.RECAPTCHA_PRIVATE_KEY,
            'remoteip': ip_address,
            'challenge': request.POST.get('recaptcha_challenge_field', ''),
            'response': request.POST.get('recaptcha_response_field', '')
        })
        captcha_req = urllib2.Request(
            url = "http://www.google.com/recaptcha/api/verify",
            data = captcha_params,
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "User-agent": "reCAPTCHA Umeqo"
            }
        )
        captcha_resp = urllib2.urlopen(captcha_req)
        return_values = captcha_resp.read().splitlines();
        captcha_resp.close()

        if return_values[0] != 'true':
            form = authentication_form(data=request.POST)
            current_site = get_current_site(request)

            context = extra_context
            context.update({
                'invalid_captcha': True,
                'form': form,
                'site': current_site,
                'site_name': current_site.name,
            })
            return context
    response = auth_login_view(request, template_name=template_name, authentication_form=AuthenticationForm, current_app=current_app, extra_context=extra_context)
    if request.user.is_staff:
        return redirect(reverse('super_login'))
    else:
        us_user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        user = request.user
        if not (is_student(user) or is_campus_org(user) or is_recruiter(user)):
            return HttpResponseServerError("User is not of any type.")
        return response
    
@login_required
@render_to('super_login.html')
@user_passes_test(is_superuser, login_url=s.LOGIN_URL)
def super_login(request, form_class = SuperLoginForm,  extra_context=None):
    if request.method == "POST":
        form = form_class(data = request.POST)
        if form.is_valid():
            if form.cleaned_data["recruiter"]:
                user = User.objects.get(username=form.cleaned_data['recruiter'])
            else:
                print CampusOrg.objects.get(name=form.cleaned_data['campus_org']).user
                user = CampusOrg.objects.get(name=form.cleaned_data['campus_org']).user
            user.backend = s.AUTHENTICATION_BACKENDS[0]
            auth_login(request, user)
            return redirect(reverse("home"))
    else:
        form = form_class()
    context = {'form':form}
    context.update(extra_context or {})
    return context

@login_required
def password_change(request, password_change_form=PasswordChangeForm, extra_context=None):
    form = password_change_form(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        request.user.userattributes.last_password_change_date = datetime.now()
        for session_key_object in request.user.sessionkey_set.all():
            Session.objects.filter(session_key=session_key_object.session_key).delete()
        request.user.sessionkey_set.all().delete()
        request.user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, request.user)
        us_user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        data = {'valid':True}
    else:
        data = {'valid':False, 'errors':form.errors}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    
@render_to('invalid_activation_link.html')
def activate_user(request, backend = RegistrationBackend(), success_url=None, extra_context=None, **context):
    user = backend.activate(request, **context)
    if user:
        user.backend = s.AUTHENTICATION_BACKENDS[0]
        auth_login(request, user)
        us_user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        if success_url is None:
            to, args, context = backend.post_activation_redirect(request, user)
            return redirect(to, *args, **context)
        else:
            return redirect(success_url)
    context.update(extra_context or {})
    return context