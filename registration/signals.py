from django.dispatch import Signal

from core.view_helpers import get_ip
from registration.models import LoginAttempt, SessionKey, UserAttributes


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])

def clear_login_attempts(sender, request, user, **kwargs):
    ip_address = get_ip(request)
    LoginAttempt.objects.all().filter(ip_address=ip_address).delete()

def delete_session_key(sender, request, user, **kwargs):
    SessionKey.objects.filter(user=user, session_key=request.session.session_key).delete()
    
def create_session_key(sender, request, user, **kwargs):
    SessionKey.objects.create(user=user, session_key=request.session.session_key)

def create_userattributes(sender, instance, created, raw, **kwargs):
    if created and not raw:
        UserAttributes.objects.create(user=instance, is_verified=False)