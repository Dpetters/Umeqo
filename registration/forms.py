from django import forms
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class PasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(label=_("Email:"), max_length=75, required=True)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(
                                email__iexact=email,
                                is_active=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("This email has no associated account."))
        return email
     
class SetPasswordForm(AuthSetPasswordForm):
    new_password1 = forms.CharField(label=_("Choose Password:"), widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(label=_("Confirm Password:"), widget=forms.PasswordInput, required=True)
    
class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(label=_("Old password:"), widget=forms.PasswordInput, required=True)
   
    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly."))
        return old_password