from django.contrib.auth import signals
from django.dispatch import Signal, receiver


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])

@receiver(signals.user_logged_in)
def clear_attempts(sender, request, user, **kwargs):
    ip_address = request.META['HTTP_X_FORWARDED_FOR']
    LoginAttempt.objects.all().filter(ip_address=ip_address).delete()
