from django import forms
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from django.utils.translation import ugettext_lazy as _

class PasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(label=_("Email:"), max_length=75)
    
class SetPasswordForm(AuthSetPasswordForm):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=_("Choose a Password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Re-Enter Password"), widget=forms.PasswordInput)
