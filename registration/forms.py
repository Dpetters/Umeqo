from django import forms
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from django.utils.translation import ugettext_lazy as _

class PasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(label=_("Email:"), max_length=75, required=True)
    
class SetPasswordForm(AuthSetPasswordForm):
    new_password1 = forms.CharField(label=_("Choose Password:"), widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(label=_("Confirm Password:"), widget=forms.PasswordInput, required=True)
    
class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(label=_("Old password:"), widget=forms.PasswordInput, required=True)
