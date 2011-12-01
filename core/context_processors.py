from django.conf import settings

from core.decorators import is_recruiter

def next(request):
    return {
        'login_next': request.GET.get('next', '/')
    } if 'next' in request.GET else {}
        
def get_current_path(request):
    return {
       'current_path': request.get_full_path().split("?")[0]
     }

def registration(request):
    return {
       'registration_open': settings.REGISTRATION_OPEN
     }

def load_wait_time(request):
    return {
        'load_wait_time':settings.LOAD_WAIT_TIME
    }
    
def employer_subscription(request):
    if is_recruiter(request.user):
        return {
        'sa': request.user.recruiter.employer.subscribed_annually,
        'subs':request.user.recruiter.employer.subscribed
        }
    return {}
