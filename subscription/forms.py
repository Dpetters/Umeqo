from django import forms

from core.decorators import is_recruiter
from employer.models import Employer

subscription_templates = {'upgrade':'subscription_body_upgrade.html',
                          'subscribe':'subscription_body_subscribe.html',
                          'cancel':'subscription_body_cancel.html'}

class SubscriptionForm(forms.Form):
    name = forms.CharField(label=u'Your Name:', max_length=100, widget=forms.TextInput())
    email = forms.EmailField(label='Your Email:', widget=forms.TextInput(attrs=dict(maxlength=200)))
    employer = forms.CharField(label='Employer Name:', max_length = 100)
    body = forms.CharField(label='Message:', widget=forms.Textarea())

    def __init__(self, user, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        if is_recruiter(user):
            self.fields['employer'] = forms.ModelChoiceField(label='Employer Name:', queryset = Employer.objects.filter(employersubscription__isnull=False))