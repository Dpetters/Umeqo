from django import forms

from core.decorators import is_recruiter
from employer.models import Employer

class SubscriptionRequestForm(forms.Form):
    recruiter_name = forms.CharField(label=u'Your Name:', max_length=100, widget=forms.TextInput())
    recruiter_email = forms.EmailField(label='Your Email:', widget=forms.TextInput(attrs=dict(maxlength=200)))
    employer_name = forms.CharField(label='Employer Name:', max_length = 100)
    message_body = forms.CharField(label='Message:', widget=forms.Textarea())
    
    def __init__(self, user, *args, **kwargs):
        super(SubscriptionRequestForm, self).__init__(*args, **kwargs)
        if is_recruiter(user):
            self.fields['employer_name'] = forms.ModelChoiceField(label='Employer Name:', initial=user.recruiter.employer, queryset = Employer.objects.filter(employersubscription__isnull=False))
            self.fields['recruiter_name'].initial  =  "%s %s" % (user.first_name, user.last_name,)
            self.fields['recruiter_email'].initial = user.email