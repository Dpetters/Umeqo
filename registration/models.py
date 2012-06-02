import datetime

from django.conf import settings as s
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.template import Context
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from core import mixins as core_mixins
from core.email import get_basic_email_context, send_email
from core.view_helpers import get_ip
from core.signals import us_user_logged_in
from registration.managers import RegistrationManager

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
    agreed_to_terms_datetime = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "User Attributes"
        verbose_name_plural = "User Attributes"
    def __unicode__(self):
        return str(self.user)

    def has_agreed_to_terms(self):
        self.agreed_to_terms = True
        self.agreed_to_terms_datetime = datetime.datetime.now()
        self.save()
        
@receiver(post_save, sender=User)
def create_userattributes(sender, instance, created, raw, **kwargs):
    if created and not raw:
        UserAttributes.objects.create(user=instance, is_verified=False)


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
        expiration_date = datetime.timedelta(days=s.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True

    def send_activation_email(self, site, first_name, last_name):
        if not first_name:
            first_name = self.user.email.split("@")[0]
        context = Context({ 'activation_key': self.activation_key,
                            'first_name': first_name})
        context.update(get_basic_email_context())

        subject = ''.join(render_to_string('email_subject.txt', {
            'message': "Account Activation"
        }, context).splitlines())
        
        text_email_body = render_to_string('activation_email.txt', context)
        html_email_body = render_to_string('activation_email.html', context)
        
        send_email(subject, text_email_body, [self.user.email], html_email_body)


class LoginAttempt(models.Model):
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(editable=False, null=True)

@receiver(user_logged_in, sender=User)
def clear_login_attempts(sender, request, user, **kwargs):
    ip_address = get_ip(request)
    if ip_address:
        LoginAttempt.objects.all().filter(ip_address=ip_address).delete()