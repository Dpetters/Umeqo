from django.conf import settings as s
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from core.decorators import is_recruiter

def next(request):
    if request.GET.has_key('next'):
        login_next = request.GET['next']
    else:
        login_next = request.get_full_path()
    return {'login_next': login_next}
        
def get_current_path(request):
    return {
       'current_path': request.get_full_path().split("?")[0]
       }

def registration(request):
    return {
       'registration_open': s.REGISTRATION_OPEN
       }

def load_wait_time(request):
    return {
        'load_wait_time':s.LOAD_WAIT_TIME
        }

def current_site(request):
    return {
        'current_site': Site.objects.get(id=s.SITE_ID)
        }

def employer_subscription(request):
    if is_recruiter(request.user):
        return {
        'sa': request.user.recruiter.employer.subscribed_annually,
        'subs':request.user.recruiter.employer.subscribed
        }
    return {}

def warnings(request):
    warnings = []
    if is_recruiter(request.user):        
        employer_subscription = request.user.recruiter.employer.employersubscription
        subscription_path = reverse("subscription_list")
        if employer_subscription.in_grace_period() and request.get_full_path() != subscription_path:
            warnings.append("Your subscription has expired - you have {0} of access left. <a href='{1}'>Renew now</a>.".format((employer_subscription.time_left()), subscription_path))
    return {'warnings':warnings}