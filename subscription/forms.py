from django import forms

from employer.models import Recruiter

subscription_dialog_parts = {'upgrade':{'title':'Upgrade Subscription', 'template':'subscription_body_upgrade.txt'},
                             'subscribe':{'title':'Subscribe to Umeqo', 'template':'subscription_body_subscribe.txt'},
                             'cancel':{'title':'Cancel Subscription', 'template':'subscription_body_cancel.txt'},
                             'downgrade':{'title':'Downgrade Subscription', 'template':'subscription_body_downgrade.txt'}}
                        
class SubscriptionForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(), label=u'Your Name:')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=200)), label=u'Your Email:')
    body = forms.CharField(widget=forms.Textarea(), label=u'Message')
    
    
class SubscriptionCancelForm(SubscriptionForm):
    new_master_recruiter = forms.ModelChoiceField(label="New Master Recruiter:", queryset = Recruiter.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(SubscriptionCancelForm, self).__init__(*args, **kwargs)
        self.fields['new_master_recruiter'].queryset = Recruiter.objects.exclude(id=kwargs.get('initial').get('recruiter_id', ''))
