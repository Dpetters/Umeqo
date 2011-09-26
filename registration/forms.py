from django import forms
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django.utils.http import int_to_base36



from core.form_helpers import decorate_bound_field
from core import messages

decorate_bound_field()

class PasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(label=_("Email:"), max_length=75, required=True)

    def clean_email(self):
        """
        Validates that a non-suspeded user exists with the given e-mail address.
        """
        try:
            user = User.objects.get(email = self.cleaned_data["email"])
        except User.DoesNotExist:
            raise forms.ValidationError(messages.email_not_registered)
        if not user.is_active and not user.userattributes.is_verified:
            raise forms.ValidationError(messages.account_suspended)
        if user.is_active and not user.userattributes.is_verified:
            raise forms.ValidationError(messages.not_activated_short)
        # Required to let the save method in AuthPasswordResetForm work
        self.users_cache = [user]
        return self.cleaned_data["email"]

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from core.email import send_html_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_html_mail("[%s] Password Reset" % site_name,
                t.render(Context(c)), [user.email])
     
class SetPasswordForm(AuthSetPasswordForm):
    pass
    
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = "Choose Password:"
        self.fields['new_password2'].label = "Confirm Password:"


class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(label=_("Old password:"), widget=forms.PasswordInput, required=True)
        
    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(messages.incorrect_old_password)
        return old_password