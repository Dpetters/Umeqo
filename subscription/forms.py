from django import forms

from core.decorators import is_recruiter
from employer.models import Employer
from subscription.choices import EMPLOYER_SIZE_CHOICES

subscription_templates = {'upgrade':'subscription_body_upgrade.html',
                          'extend':'subscription_body_extend.html',
                          'subscribe':'subscription_body_subscribe.html'}

class SubscriptionForm(forms.Form):
    recruiter_name = forms.CharField(label=u'Your Name:', max_length=100, widget=forms.TextInput())
    recruiter_email = forms.EmailField(label='Your Email:', widget=forms.TextInput(attrs=dict(maxlength=200)))
    employer_name = forms.CharField(label='Employer Name:', max_length = 100)
    employer_size = forms.ChoiceField(label="Employer Size:", choices = EMPLOYER_SIZE_CHOICES)
    message_body = forms.CharField(label='Message:', widget=forms.Textarea())
    
    def __init__(self, user, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        if is_recruiter(user):
            self.fields['employer_name'] = forms.ModelChoiceField(label='Employer Name:', initial=user.recruiter.employer, queryset = Employer.objects.filter(employersubscription__isnull=False))
            self.fields['recruiter_name'].initial  =  "%s %s" % (user.first_name, user.last_name,)
            self.fields['recruiter_email'].initial = user.email
            self.fields['employer_size'].initial = user.recruiter.employer.size