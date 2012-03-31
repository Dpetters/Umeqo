import stripe

from django.http import HttpResponse
from django.conf import settings as s
from django.utils import simplejson
from django.template.loader import render_to_string

from core.email import send_html_mail
from core.decorators import is_recruiter, render_to
from subscription.models import EmployerSubscription
from subscription.forms import CardForm, SubscriptionRequestForm


@render_to("subscription_request_dialog.html")
def subscription_request_dialog(request, form_class = SubscriptionRequestForm, extra_context=None):
    if request.method=="POST":
        form = form_class(data = request.POST, user=request.user)
        if form.is_valid():
            data = []
            recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
            subject = "[Umeqo Sales] %s Subscription Request" % (form.cleaned_data['employer_name'])
            subscription_email_context = {'form':form}
            html_body = render_to_string('subscription_request_body.html', subscription_email_context)
            send_html_mail(subject, html_body, recipients)
        else:
            data = {'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        subscription_type = request.GET.get('subscription_type', 'basic')
        initial = {'message_body':render_to_string("I would like to sign up for Umeqo {{subscription_type}}. Please validate that I'm an actual employer and send me my credentials.", {'subscription_type':subscription_type})}
        context = {'form':form_class(initial=initial, user=request.user)}
        context.update(extra_context or {})
        return context


@render_to("subscription_upgrade.html")
def subscription_upgrade(request, subscription_type, form_class=CardForm, extra_context=None):
    context = {}
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            employer = request.user.recruiter.employer
            token = request.POST['stripeToken']
            if employer.stripe_id:
                customer = stripe.Customer.retrieve(
                    employer.stripe_id
                    )
            else:
                customer = stripe.Customer.create(
                    card=token,
                    plan="premium",
                    email=request.user.email
                )
                employer.stripe_id = customer.id
            employer.card = form.cleaned_data['stripe_token']
            employer.last_4_digits = form.cleaned_data['last_4_digits']
            customer.save()
    else:
        context['form'] = form_class()
    context.update(extra_context or {})
    return context

@render_to("subscription_change_payment.html")
def subscription_change_payment(request, extra_context=None):
    context = {}
    return context

@render_to("subscription_cancel.html")
def subscription_cancel(request, subscription_type, extra_context=None):
    context = {'subscription_type':subscription_type}
    return context

@render_to("subscription_cancel.html")
def subscription_cancel_confirm(request, extra_context=None):
    context = {}
    return context

@render_to("subscription_list.html")
def subscription_list(request, extra_context=None):
    context = {}
    """
    This page is only customized if the user is a recruiter.
    
    If they have an active premium subscription, the basic button theyn says "Downgrade to Basic"
    and the premium button says "Extend Premium Subscription"
    
    If they have don't have a premium subscription, the basic button says
    "Basic Subscription Active".
    """

    employer = None
    premium_subscription = None
    if request.user.is_authenticated() and is_recruiter(request.user):
        employer = request.user.recruiter.employer
        try:
            premium_subscription = employer.employersubscription
        except EmployerSubscription.DoesNotExist:
            premium_subscription = None
    
    if employer:
        if premium_subscription and not premium_subscription.expired():
            context['paid_subscription_button_text'] = "Extend Subscription"
            
            context['subscription_request_dialog_title'] = "Extend Subscription"
            context['paid_subscription_action'] = "extend"
            context['paid_subscription_text'] = "Subscription Expired"
            context["free_subcription_dialog_href"] = "downgrade"
            
            context["free_subscription_button_text"] = "Downgrade to Basic"
        else:
            context["free_subscription_button_text"] = "Basic Subscription Active"
            
    else:
        context["free_subcription_dialog_class"] = "open_subscription_request_dialog"
    context.update(extra_context or {})
    return context