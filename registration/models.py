import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from core import mixins as core_mixins
from core.decorators import is_student
from core.view_helpers import get_ip
from events.models import Event
from registration.managers import RegistrationManager
from notification.models import NoticeType
from employer.models import Employer
from notification import models as notification


class InterestedPerson(core_mixins.DateTracking):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField("Contact E-mail", blank=True, null=True, unique=True)
    summer_plans = models.CharField("Summer plans?",max_length=200, null=True, blank=True)
    ip_address = models.IPAddressField(editable=False, null=True)
    auto_email = models.BooleanField(default=False)
    final = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Interested Person"
        verbose_name_plural = "Interested Persons"
        
    def __unicode__(self):
        return self.first_name + " " + self.last_name


class SessionKey(core_mixins.DateTracking):
    session_key = models.CharField('Session Key', max_length=40, editable=False)
    user = models.ForeignKey(User, editable=False)
    
    class Meta:
        verbose_name = "Session Key"
        verbose_name_plural = "Session Keys"
        
    def __unicode__(self):
        return str(self.user)

@receiver(user_logged_out, sender=User)
def delete_session_key(sender, request, user, **kwargs):
    SessionKey.objects.filter(user=user, session_key=request.session.session_key).delete()

@receiver(user_logged_in, sender=User)
def create_session_key(sender, request, user, **kwargs):
    SessionKey.objects.create(user=user, session_key=request.session.session_key)
    
class UserAttributes(models.Model):
    user = models.OneToOneField(User)
    is_verified = models.BooleanField(default=False)
    last_password_change_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "User Attributes"
        verbose_name_plural = "User Attributes"

    def __unicode__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_userattributes(sender, instance, created, raw, **kwargs):
    if created and not raw:
        UserAttributes.objects.create(user=instance, is_verified=True)


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.
    
    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.
    
    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.
    
    """
    ACTIVATED = u"ALREADY_ACTIVATED"
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    
    objects = RegistrationManager()
    
    class Meta:
        verbose_name = _('Registration Profile')
        verbose_name_plural = _('Registration Profiles')
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        
        Key expiration is determined by a two-step process:
        
        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True

    def send_activation_email(self, site):
        """
        Send an activation email to the user associated with this
        ``RegistrationProfile``.
        
        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = { 'activation_key': self.activation_key,
                     'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                     'site': site }
        subject = render_to_string('activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('activation_email.txt', ctx_dict)
        
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

class LoginAttempt(models.Model):
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(editable=False, null=True)

@receiver(user_logged_in, sender=User)
def clear_login_attempts(sender, request, user, **kwargs):
    ip_address = get_ip(request)
    if ip_address:
        LoginAttempt.objects.all().filter(ip_address=ip_address).delete()

@receiver(post_save, sender=User)
def send_first_notice(sender, instance, created, raw, **kwargs):
    if created and is_student(sender) and not raw:
        try:
            event = Event.objects.get(id=settings.WELCOME_EVENT_ID)
            employer = Employer.objects.get(name="Umeqo")
            message = "This is your first invite! There are many more to come!"
            notification.send([sender], "public_invite", {
                'employer_name': str(employer.name),
                'employer_url': employer.get_absolute_url,
                'invite_message': message,
                'event': event
            })
        except Event.DoesNotExist:
            pass