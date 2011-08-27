from django.contrib.auth import signals
from django.dispatch import Signal, receiver

from core.view_helpers import get_ip
from registration.models import LoginAttempt


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])

@receiver(signals.user_logged_in)
def clear_attempts(sender, request, user, **kwargs):
    ip_address = get_ip(request)
    LoginAttempt.objects.all().filter(ip_address=ip_address).delete()
