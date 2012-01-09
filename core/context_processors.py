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

# Cautions are orange. Warnings are red.
def caution(request):
    cautions = []
    if is_recruiter(request.user) and hasattr(request.user.recruiter.employer, "employersubscription"):
        employer_subscription = request.user.recruiter.employer.employersubscription
        subscription_path = reverse("subscription_list")
        if employer_subscription.in_grace_period():
            action_wording = "Renew now"
            if employer_subscription.subscription.uid == s.EVENT_SUBSCRIPTION_UID:
                action_wording = "Upgrade now"
            if request.get_full_path() != subscription_path:
                cautions.append("Your {2} has expired - you have {0} of access left. <a href='{1}'>{3}</a>.".format(employer_subscription.time_left(), subscription_path, employer_subscription.subscription, action_wording))
            else:
                cautions.append("Your {1} has expired - you have {0} of access left. {2}.".format(employer_subscription.time_left(), employer_subscription.subscription, action_wording))
    return {'cautions':cautions}

def warnings(request):
    warnings = []
    if is_recruiter(request.user) and hasattr(request.user.recruiter.employer, "employersubscription"):        
        employer_subscription = request.user.recruiter.employer.employersubscription
        subscription_path = reverse("subscription_list")
        if employer_subscription.expired():
            if request.get_full_path() != subscription_path:
                if employer_subscription.subscription.uid == s.EVENT_SUBSCRIPTION_UID:
                    warnings.append("Your {0} has expired. Please host another campus event or <a href='{1}'>upgrade now</a> to regain access.".format(employer_subscription.subscription, subscription_path))
                else:
                    warnings.append("Your {0} has expired. Please <a href='{1}'>renew it</a> to regain access.".format(employer_subscription.subscription, subscription_path))
            else:
                if employer_subscription.subscription.uid == s.EVENT_SUBSCRIPTION_UID:
                    warnings.append("Your {0} has expired. Please host another campus event or upgrade now to regain access.".format(employer_subscription.subscription))
                else:
                    warnings.append("Your {0} has expired. Please renew it to regain access.".format(employer_subscription.subscription))
    return {'warnings':warnings}