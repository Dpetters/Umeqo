from django import forms

from employer.models import Recruiter

subscription_templates = {'upgrade':'subscription_body_upgrade.html',
                          'subscribe':'subscription_body_subscribe.html',
                          'cancel':'subscription_body_cancel.html'}
                        
class SubscriptionForm(forms.Form):
    name = forms.CharField(label=u'Your Name:', max_length=100, widget=forms.TextInput())
    email = forms.EmailField(label='Your Email:', widget=forms.TextInput(attrs=dict(maxlength=200)))
    employer = forms.CharField(label='Employer Name:', max_length = 42)
    body = forms.CharField(label='Message:', widget=forms.Textarea())