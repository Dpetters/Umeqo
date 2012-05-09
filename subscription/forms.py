import stripe

from django import forms
from django.conf import settings as s
from django.forms import RadioSelect

from core.http import Http500
from core.templatetags.filters import format_money
from subscription import choices as subscription_choices
from subscription.models import Subscription


class SubscriptionChangeForm(forms.Form):
    subscription_type = forms.ModelChoiceField(
        queryset = Subscription.objects.all().order_by("uid"),
        required=True
    )
    billing_period = forms.ChoiceField(
        choices = subscription_choices.BILLING_CYCLE_CHOICES,
        required=True
        )

            
class AccountRequestForm(forms.Form):
    recruiter_name = forms.CharField(
         label=u'Your Name:',
         max_length=100,
         widget=forms.TextInput()
    )
    recruiter_email = forms.EmailField(
        label='Your Email:',
        widget=forms.TextInput(attrs=dict(maxlength=200))
    )
    employer_name = forms.CharField(
        label='Employer Name:',
        max_length = 100
    )
    message_body = forms.CharField(
        label='Message:',
        widget=forms.Textarea()
    )

class CardForm(forms.Form):
    stripe_token = forms.CharField(
        required = True,
        widget = forms.HiddenInput()
    )

class ChangeBillingForm(CardForm):
    billing_cycle = forms.ChoiceField(
        choices=(),
        widget=RadioSelect,
        initial="year",
        required=True
    )

    stripe_token = forms.CharField(
        required = False,
        widget = forms.HiddenInput()
    )
    
    def __init__(self, subscription_type, current_billing_cycle, *args, **kwargs):
        super(ChangeBillingForm, self).__init__(*args, **kwargs)
        stripe.api_key = s.STRIPE_SECRET
        billing_cycle_choices = []
        if subscription_type in s.SUBSCRIPTION_UIDS.keys():
            billing_cycles = s.SUBSCRIPTION_UIDS[subscription_type]
            monthly_price = None
            for billing_cycle, value in billing_cycles.items():
                times, plan_stripe_id = value 
                plan = stripe.Plan.retrieve(plan_stripe_id)
                amount = plan.amount
                string = "Bill me %s per %s" % (format_money(plan.amount), billing_cycle)

                if billing_cycle == "month":
                    monthly_price = amount
                elif monthly_price:
                    percentage = int((1.0-amount/float(monthly_price*times))*100)
                    string += " (save %d%%)" % (percentage) 

                if current_billing_cycle != billing_cycle and not(current_billing_cycle == "year" and billing_cycle == "month"):
                    billing_cycle_choices.append((billing_cycle, string))
                    
            self.fields['billing_cycle'].choices = billing_cycle_choices
        else:
            raise Http500("Unhandled subscription type: %s" % subscription_type)

class CheckoutForm(ChangeBillingForm):
    stripe_token = forms.CharField(
        required = False,
        widget = forms.HiddenInput()
    )