from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from core.decorators import render_to
from campus_org.models import CampusOrg


@login_required
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
