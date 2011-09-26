from __future__ import division
from __future__ import absolute_import

from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import simplejson
from django.views.decorators.http import require_POST, require_GET

from core.decorators import is_campus_org, render_to
from registration.forms import PasswordChangeForm
from core import messages
from campus_org.models import CampusOrg
from campus_org.forms import CampusOrgPreferencesForm, CampusOrgProfileForm


@login_required
@user_passes_test(is_campus_org, login_url=s.LOGIN_URL)
@render_to("campus_org_account.html")
@require_GET
def campus_org_account(request, preferences_form_class = CampusOrgPreferencesForm, 
                     change_password_form_class = PasswordChangeForm, extra_context=None):
    context = {}
    msg = request.GET.get('msg', None)
    if msg:
        page_messages = {
            'password-changed': messages.password_changed,
        }
        context["msg"] = page_messages[msg]
    context['preferences_form'] = preferences_form_class(instance=request.user.campusorg)
    context['change_password_form'] = change_password_form_class(request.user)
    context.update(extra_context or {})
    return context


@login_required
@user_passes_test(is_campus_org)
@require_POST
def campus_org_account_preferences(request, form_class=CampusOrgPreferencesForm):
    form = form_class(data=request.POST, instance=request.user.campusorg)
    data = []
    if form.is_valid():
        request.user.recruiter.recruiter_preferencess = form.save()
    else:
        data = {'errors': form.errors }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@login_required
@user_passes_test(is_campus_org, login_url=s.LOGIN_URL)
@render_to("campus_org_profile.html")
def campus_org_profile(request, form_class=CampusOrgProfileForm, extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=request.user.campusorg)
        data = {}
        if form.is_valid():
            form.save()
        else:
            data['errors'] = form.errors
        return HttpResponse(simplejson.dumps(data), mimetype="text/html")
    else:
        context = {'form':form_class(instance=request.user.campusorg), 'edit':True}
        context.update(extra_context or {})
        return context
    
@render_to('campus_org_info.html')
def campus_org_info(request, extra_context = None):
    if request.is_ajax():
        if request.GET.has_key('campus_org_id'):
            try:
                context = {}
                context['campus_org'] = CampusOrg.objects.get(id=request.GET['campus_org_id'])
                context.update(extra_context or {})
                return context
            except CampusOrg.DoesNotExist:
                return HttpResponseBadRequest("Campus Org ID doesn't match any existing campus org's ID.")        
        else:
            return HttpResponseBadRequest("Campus Org ID is missing")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")


@login_required
def check_campus_org_uniqueness(request):
    if request.is_ajax():
        try:
            CampusOrg.objects.get(name=request.GET.get("name"))
            return HttpResponse(simplejson.dumps(False), mimetype="application/json")
        except CampusOrg.DoesNotExist:
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponseForbidden("Request must be a valid XMLHttpRequest")
