from django import forms

class RegistrationForm(forms.Form):

    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data