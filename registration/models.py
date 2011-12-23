import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from student.models import Student
from core import mixins as core_mixins
from core.view_helpers import get_ip
from core.signals import us_user_logged_in
from events.models import Event
from registration.managers import RegistrationManager
from notification.models import NoticeType
from employer.models import Employer
from core.email import send_html_mail
from notification import models as notification

class RegException(core_mixins.DateCreatedTracking):
    email = models.EmailField("E-mail to allow:", unique=True)

    class Meta:
        verbose_name = "Registration Exception"
        verbose_name_plural = "Registration Exceptions"
        
    def __unicode__(self):
        return self.email
    
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

@receiver(us_user_logged_in, sender=User)
def create_session_key(sender, request, user, **kwargs):
    SessionKey.objects.create(user=user, session_key=request.session.session_key)
    
class UserAttributes(models.Model):
    user = models.OneToOneField(User)
    is_verified = models.BooleanField(default=False)
    last_password_change_date = models.DateTimeField(blank=True, null=True)
    agreed_to_terms = models.BooleanField(default=False)
    agreed_to_terms_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "User Attributes"
        verbose_name_plural = "User Attributes"

    def __unicode__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_userattributes(sender, instance, created, raw, **kwargs):
    if created and not raw:
        UserAttributes.objects.create(user=instance, is_verified=False, agreed_to_terms=True)


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

    def send_activation_email(self, site, first_name, last_name):
        subject = "[umeqo.com] Account Activation"
        context = { 'activation_key': self.activation_key, 'site': site, 'first_name':first_name, 'last_name':last_name}
        message = render_to_string('activation_email.html', context)
        send_html_mail(subject, message, [self.user.email])

class LoginAttempt(models.Model):
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(editable=False, null=True)

@receiver(user_logged_in, sender=User)
def clear_login_attempts(sender, request, user, **kwargs):
    ip_address = get_ip(request)
    if ip_address:
        LoginAttempt.objects.all().filter(ip_address=ip_address).delete()

@receiver(post_save, sender=Student)
def send_first_notice(sender, instance, created, raw, **kwargs):
    if created and not raw:
        try:
            event = Event.objects.get(id=settings.WELCOME_EVENT_ID)
            employer = Employer.objects.get(name="Umeqo")
            recruiter = User.objects.get(id=settings.UMEQO_RECRUITER_ID)
            notice_type = NoticeType.objects.get(label="public_invite")
            invite_message = "Congrats on your first invite! There are many more to come!"
            notification.send([instance.user], notice_type, {
                'employer': employer,
                'recruiter': recruiter,
                'invite_message': invite_message,
                'event': event,
                'name': instance.user.first_name
            })
        except Event.DoesNotExist:
            pass