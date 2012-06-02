from django import forms
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, \
                                      SetPasswordForm as AuthSetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template import Context, loader
from django.template.loader import render_to_string
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from auth.form_helpers import verify_account

from core import messages as m
from core.email import get_basic_email_context, send_email
from core.form_helpers import decorate_bound_field

decorate_bound_field()

class PasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(label=_("Email:"), max_length=75, required=True)

    def clean_email(self):
        try:
            user = User.objects.get(email = self.cleaned_data["email"])
        except User.DoesNotExist:
            raise forms.ValidationError(m.email_not_registered)

        verify_account(user)

        # Required to let the save method in AuthPasswordResetForm work
        self.users_cache = [user]
        return self.cleaned_data["email"]

    def save(self, domain_override=None,
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, 
             request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        for user in self.users_cache:
            html_email_template_name = email_template_name
            text_email_template_name='password_reset_email.txt'
            text_email_body_template = loader.get_template(text_email_template_name)
            html_email_body_template = loader.get_template(html_email_template_name)
            
            context = Context({
                'email': user.email,
                'uid': int_to_base36(user.id),
                'first_name': user.first_name,
                'token': token_generator.make_token(user),
            })
            context.update(get_basic_email_context())

            subject = ''.join(render_to_string('email_subject.txt', {
                'message': "Password Reset"
            }, context).splitlines())
        
            text_email_body = text_email_body_template.render(Context(context)) 
            html_email_body = html_email_body_template.render(Context(context))

            send_email(subject, text_email_body, [user.email], html_email_body)


class SetPasswordForm(AuthSetPasswordForm):
    pass
    
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = "Choose Password:"
        self.fields['new_password2'].label = "Confirm Password:"

class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(label=_("Old password:"), widget=forms.PasswordInput, 
                                   required=True)
        
    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(m.incorrect_old_password)
        return old_password