from datetime import datetime, timedelta
import urllib
import urllib2

from django.conf import settings as s
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth.models import User, update_last_login
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import login as auth_login_view, logout as auth_logout_then_login_view
from django.contrib.sessions.models import Session
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson

from campus_org.models import CampusOrg
<<<<<<< HEAD
from core.http import Http403, Http500
from core.decorators import render_to, is_superuser
=======
from core.decorators import render_to
>>>>>>> master
from core.forms import EmailAuthenticationForm as AuthenticationForm, SuperLoginForm
from core.view_helpers import get_ip
from core.signals import us_user_logged_in
from events.models import Event
from registration.models import LoginAttempt
from registration.backend import RegistrationBackend
from registration.forms import PasswordChangeForm
from notification.models import NoticeType
from employer.models import Employer
from notification import models as notification


def logout(request, login_url=None, current_app=None, extra_context=None):
    return auth_logout_then_login_view(request, login_url, current_app, extra_context)


@render_to('login.html')
def login(request, template_name="login.html", authentication_form=AuthenticationForm, login_url=None, current_app=None, extra_context={}):
    try:
        user = authenticate(username='recruiter@umeqo.com', password='umeqodemo')
        auth_login(request, user)
    except:
        raise Http500('The demo authentication server is currently unavailable')

    return redirect(reverse("home"))


@render_to('super_login.html')
@user_passes_test(lambda x: x.is_superuser)
def super_login(request, form_class = SuperLoginForm,  extra_context=None):
    if request.method == "POST":
        form = form_class(data = request.POST)
        if form.is_valid():
            if form.cleaned_data["recruiter"]:
                user = User.objects.get(username=form.cleaned_data['recruiter'])
            else:
                user = CampusOrg.objects.get(name=form.cleaned_data['campus_org']).user
            user.backend = s.AUTHENTICATION_BACKENDS[0]
            user_logged_in.disconnect(update_last_login)
            auth_login(request, user)
            return redirect(reverse("home"))
    else:
        form = form_class()
    context = {'form':form}
    context.update(extra_context or {})
    return context


@login_required
def password_change(request, password_change_form=PasswordChangeForm, extra_context=None):
    raise Http403('This service is disabled in the demo')


@render_to('invalid_activation_link.html')
def activate_user(request, backend = RegistrationBackend(), success_url=None, extra_context=None, **context):
    user = backend.activate(request, **context)
    if user:
        try:
            event = Event.objects.get(id=s.WELCOME_EVENT_ID)
            employer = Employer.objects.get(name="Umeqo")
            recruiter = User.objects.get(id=s.UMEQO_RECRUITER_ID)
            notice_type = NoticeType.objects.get(label="public_invite")
            invite_message = 'Welcome to Umeqo! Recruiters can now send you invitations to events, and this is an example of one. To learn more, click "RSVP Attending" below.'
            notification.send([user], notice_type, {
                'employer': employer,
                'recruiter': recruiter,
                'invite_message': invite_message,
                'event': event,
                'name': user.first_name
            })
        except Event.DoesNotExist:
            pass
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