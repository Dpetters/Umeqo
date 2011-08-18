from django import forms
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from core import messages


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
        # Required to let the save method in AuthPasswordResetForm work
        self.users_cache = [user]
        return self.cleaned_data["email"]

     
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