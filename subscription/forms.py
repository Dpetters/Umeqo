from django import forms

from employer.models import Recruiter
from employer.choices import EMPLOYER_TYPE_CHOICES

subscription_templates = {'upgrade':'subscription_body_upgrade.html',
                          'subscribe':'subscription_body_subscribe.html',
                          'cancel':'subscription_body_cancel.html'}
                        
class SubscriptionForm(forms.Form):
    name = forms.CharField(label=u'Your Name:', max_length=100, widget=forms.TextInput())
    email = forms.EmailField(label='Your Email:', widget=forms.TextInput(attrs=dict(maxlength=200)))
    employer = forms.CharField(label='Your Employer:', max_length = 42)
    employer_type = forms.ChoiceField(label='Employer Type:', choices=EMPLOYER_TYPE_CHOICES)
    body = forms.CharField(label='Message:', widget=forms.Textarea())
    
class SubscriptionCancelForm(SubscriptionForm):
    new_master_recruiter = forms.ModelChoiceField(label="New Master Recruiter:", queryset = Recruiter.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(SubscriptionCancelForm, self).__init__(*args, **kwargs)
        self.fields['new_master_recruiter'].queryset = Recruiter.objects.exclude(id=kwargs.get('initial').get('recruiter_id', ''))