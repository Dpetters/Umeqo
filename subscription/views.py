import stripe
import time

from django.http import HttpResponse
from django.conf import settings as s
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from core.email import send_html_mail
from core.decorators import is_recruiter, render_to
from subscription.forms import CardForm, SubscriptionChangeForm, SubscriptionRequestForm


@render_to("account_request_dialog.html")
def account_request(request, form_class = SubscriptionRequestForm, extra_context=None):
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

@user_passes_test(is_recruiter)
@render_to("subscription_change.html")
def subscription_change(request, form_class=SubscriptionChangeForm, extra_context=None):
    context = {}
    if request.method == 'POST':
        form = form_class(request.POST)
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

@render_to("payment_change.html")
def payment_change(request, form_class=CardForm, extra_context=None):
    context = {}
    stripe.api_key = s.STRIPE_SECRET
    employer = request.user.recruiter.employer
    if employer.stripe_id:
        customer = stripe.Customer.retrieve(
            employer.stripe_id
            )
    else:
        customer = stripe.Customer.create(
            email=request.user.email
        )
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            token = request.POST['stripe_token']
            if not customer:
                customer = stripe.Customer.create(
                    card=token,
                    email=request.user.email
                )
                employer.stripe_id = customer.id
            customer.card = form.cleaned_data['stripe_token']
            customer.save()
            employer.card = form.cleaned_data['stripe_token']
            employer.save()
            return redirect(reverse('employer_account'))
        context['form'] = form
    else:
        context['form'] = form_class()
        context['customer'] = customer
    context.update(extra_context or {})
    return context


@render_to("payment_forget.html")
def payment_forget(request, extra_context=None):
    context = {}
    stripe.api_key = s.STRIPE_SECRET
    employer = request.user.recruiter.employer
    if employer.stripe_id:
        customer = stripe.Customer.retrieve(
            employer.stripe_id
            )
    else:
        customer = stripe.Customer.create(
            email=request.user.email
        )
    if request.method == 'POST':
        customer.card = None
        a = customer.save()
        print a
        return HttpResponse()
    else:
        context['customer'] = customer
    context.update(extra_context or {})
    return context


@render_to("checkout.html")
def checkout(request, plan, form_class=CardForm, extra_context=None):
    stripe.api_key = s.STRIPE_SECRET
    plan = stripe.Plan.retrieve(plan)
    amount =  '{:.2f}'.format(plan.amount/100)
    context = {'plan':plan,
               'amount':amount}
    employer = request.user.recruiter.employer
    if employer.stripe_id:
        customer = stripe.Customer.retrieve(
            employer.stripe_id
            )
        context['customer'] = customer
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            employer = request.user.recruiter.employer
            token = request.POST['stripe_token']
            if not customer:
                customer = stripe.Customer.create(
                    card=token,
                    plan=plan,
                    email=request.user.email
                )
                employer.stripe_id = customer.id
            employer.card = form.cleaned_data['stripe_token']
            employer.last_4_digits = form.cleaned_data['last_4_digits']
            employer.save()
    else:
        context['form'] = form_class()
    context.update(extra_context or {})
    return context

@render_to("subscription_cancel.html")
def subscription_cancel(request, extra_context=None):
    context = {}
    stripe.api_key = s.STRIPE_SECRET
    employer = request.user.recruiter.employer
    if employer.stripe_id:
        customer = stripe.Customer.retrieve(
            employer.stripe_id
            )
    if request.method == "POST":
        customer.cancel_subscription(at_period_end=False)
        return redirect("%s%s" % (reverse("employer_account"), "?msg=subscription-cancelled&tab=subscription"))
    else:
        context['expiration_datetime'] = time.strftime("%m/%d/%Y", time.gmtime(customer.subscription.current_period_end))
        context['customer'] = customer
    return context

@render_to("subscriptions.html")
def subscriptions(request, extra_context=None):
    context = {}
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
        context["free_subcription_dialog_class"] = "request_account"
    """
    context.update(extra_context or {})
    return context