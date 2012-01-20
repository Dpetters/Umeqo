from __future__ import division
from __future__ import absolute_import

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.views.decorators.http import require_POST, require_GET

from campus_org.forms import CampusOrgPreferencesForm, CampusOrgProfileForm
from campus_org.models import CampusOrg
from core import messages
from core.decorators import is_campus_org, render_to, agreed_to_terms
from core.http import Http400, Http403
from registration.forms import PasswordChangeForm


@agreed_to_terms
@user_passes_test(is_campus_org)
@require_GET
@render_to("campus_org_account.html")
def campus_org_account(request, preferences_form_class = CampusOrgPreferencesForm, change_password_form_class = PasswordChangeForm, extra_context=None):
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


@agreed_to_terms
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


@agreed_to_terms
@user_passes_test(is_campus_org)
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


@require_GET
@render_to('campus_org_info.html')
def campus_org_info(request, extra_context = None):
    if not request.is_ajax():
        raise Http403("Request must be a valid XMLHttpRequest.")
    if not request.GET.has_key('campus_org_id'):
        raise Http400("Request is missing the campus_org_id.")
    try:
        id = request.GET['campus_org_id']
        campus_org = CampusOrg.objects.get(id=id)
    except CampusOrg.DoesNotExist:
        raise Http404("Campus organization with id %s doesn't exist." % id)
    context = {}
    context['campus_org'] = campus_org
    context.update(extra_context or {})
    return context


@login_required
def check_campus_org_uniqueness(request):
    if not request.is_ajax():
        raise Http403("Request must be a valid XMLHttpRequest.")
    try:
        CampusOrg.objects.get(name=request.GET.get("name"))
        return HttpResponse(simplejson.dumps(False), mimetype="application/json")
    except CampusOrg.DoesNotExist:
        return HttpResponse(simplejson.dumps(True), mimetype="application/json")