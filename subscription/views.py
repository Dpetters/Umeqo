import os
import stripe


from django.http import HttpResponse, Http404
from django.conf import settings as s
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from pyPdf import PdfFileWriter, PdfFileReader
from stripe import InvalidRequestError

from core.decorators import render_to
from core.http import Http403
from employer.decorators import is_recruiter
from employer.models import Employer
from subscription.forms import CheckoutForm, ChangeBillingForm, CardForm, SubscriptionChangeForm, AccountRequestForm
from subscription.signals import *
from subscription.utils import get_subscription_type
from time import time

def _try_to_get_customer_from_customer_id(stripe_customer_id):
    try:
        return Employer.objects.get(stripe_id=stripe_customer_id)
    except:
        return None

@csrf_exempt
def webhooks(request):
    """
    Handles all known webhooks from stripe, and calls signals.
    Plug in as you need.
    """
    
    if request.method != "POST":
        return HttpResponse("Invalid Request.", status=400)
    
    json = simplejson.loads(request.POST["json"])
    
    if json["event"] == "recurring_payment_failed":
        webhook_recurring_payment_failed.send(sender=None, customer=_try_to_get_customer_from_customer_id(json["customer"]), full_json=json)
    elif json["event"] == "invoice_ready":
        webhook_invoice_ready.send(sender=None, customer=_try_to_get_customer_from_customer_id(json["customer"]), full_json=json)
    elif json["event"] == "recurring_payment_succeeded":
        webhook_recurring_payment_succeeded.send(sender=None, customer=_try_to_get_customer_from_customer_id(json["customer"]), full_json=json)
    elif json["event"] == "subscription_trial_ending":
        webhook_subscription_trial_ending.send(sender=None, customer=_try_to_get_customer_from_customer_id(json["customer"]), full_json=json)
    elif json["event"] == "subscription_final_payment_attempt_failed":
        webhook_subscription_final_payment_attempt_failed.send(sender=None, customer=_try_to_get_customer_from_customer_id(json["customer"]), full_json=json)
    elif json["event"] == "ping":
        webhook_subscription_ping_sent.send(sender=None)
    else:
        return HttpResponse(status=400)
    
    return HttpResponse(status=200)


@csrf_exempt
def webhooks_v2(request):
    """
    Handles all known webhooks from stripe, and calls signals.
    Plug in as you need.
    """
    if request.method != "POST":
        return HttpResponse("Invalid Request.", status=400)

    event_json = simplejson.loads(request.raw_post_data)
    event_key = event_json['type'].replace('.', '_')

    if event_key in WEBHOOK_MAP:
        WEBHOOK_MAP[event_key].send(sender=None, full_json=event_json)

    return HttpResponse(status=200)


@render_to("account_request_dialog.html")
def account_request(request, form_class = AccountRequestForm, extra_context=None):
    if request.method=="POST":
        form = form_class(data = request.POST)
        if form.is_valid():
            data = []
            recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
            subject = "[Umeqo Sales] %s Account Request" % (form.cleaned_data['employer_name'])
            subscription_email_context = {'form':form}
            html_body = render_to_string('account_request_email.html', subscription_email_context)
            send_html_mail(subject, html_body, recipients)
        else:
            data = {'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        context = {}
        subscription_type = request.GET.get('subscription_type', 'basic')
        initial = {'message_body':render_to_string('account_request_body.html', {'subscription_type':subscription_type})}
        context['form'] = form_class(initial=initial)
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

@user_passes_test(is_recruiter)
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


@user_passes_test(is_recruiter)
@render_to("payment_change.html")
def payment_change(request, form_class=CardForm, extra_context=None):
    context = {}
    stripe.api_key = s.STRIPE_SECRET
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            customer.card = form.cleaned_data['stripe_token']
            customer.save()
            return redirect("%s%s" % (reverse('employer_account'), "?msg=payment-changed&tab=subscription"))
    else:
        form = form_class()
    context['form'] = form
    context['customer'] = customer
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
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
        customer.save()
        return HttpResponse()
    else:
        context['customer'] = customer
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
@render_to("checkout.html")
def checkout(request, plan, form_class=CheckoutForm, extra_context=None):
    context = {}
    customer = request.META.get('customer', None)

    try:
        plan_uids = map(lambda x: x[1], s.SUBSCRIPTION_UIDS[plan].values()) 
    except KeyError as e:
        raise Http403("You cannot upgrade to the %s plan." % plan)
    
    if customer.subscription and customer.subscription.plan.id in plan_uids:
        return redirect(reverse("subscription_change"))
    
    if request.method == 'POST':
        form = form_class(plan, None, request.POST)
        if form.is_valid():
            token = form.cleaned_data['stripe_token']
            card = None
            if token:
                card = token
            billing_cycle = form.cleaned_data['billing_cycle']
            customer.update_subscription(plan=s.SUBSCRIPTION_UIDS[plan][billing_cycle][1], card=card)
            return redirect("%s%s" % (reverse('employer_account'), "?msg=upgraded_to_premium&tab=subscription"))
    else:
        form = form_class(plan, None)
        context['customer'] = customer
    context['form'] = form
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
@render_to("subscription_billing_cycle_change.html")
def subscription_billing_cycle_change(request, form_class=ChangeBillingForm, extra_context=None):
    context = {}
    customer = request.META['customer']
    context['customer'] = customer
    if not request.META['has_at_least_premium']:
        return redirect(reverse("subscription_change"))
    plan = get_subscription_type(customer.subscription.plan.id)
    if request.method == 'POST':
        form = form_class(plan, customer.subscription.plan.interval, request.POST)
        if form.is_valid():
            token = form.cleaned_data['stripe_token']
            card = None
            if token:
                card = token
            billing_cycle = form.cleaned_data['billing_cycle']
            customer.update_subscription(plan=s.SUBSCRIPTION_UIDS[plan][billing_cycle][1], card=card)
            customer.save()
            return redirect("%s%s" % (reverse('employer_account'), "?msg=changed_billing&tab=subscription"))
    else:
        form = form_class(plan, customer.subscription.plan.interval)
        # TODO - allow for the price computation to be more flexible (beyond just an upgrade
        # from a monthly subscription to an annual subscription
        premium_annual_subscription_id = s.SUBSCRIPTION_UIDS['premium']['year'][1]
        premium_monthly_subscription_id = s.SUBSCRIPTION_UIDS['premium']['month'][1]
        annual_plan = stripe.Plan.retrieve(premium_annual_subscription_id)
        annual_plan_amount = annual_plan.amount
        monthly_plan = stripe.Plan.retrieve(premium_monthly_subscription_id)
        monthly_plan_amount = monthly_plan.amount
        refund = monthly_plan_amount * (1-(time() - customer.subscription['start'])/(customer.subscription['current_period_end'] - customer.subscription['start']))
        context['refund'] = refund
        context['annual_plan_amount'] = annual_plan_amount
        context['prorated_amount'] = annual_plan_amount - refund 
    context['form'] = form
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
def receipt_view(request, charge_id):
    customer = request.META.get('customer', None)
    employer = request.user.recruiter.employer
    
    try:
        charge_ids = map(lambda x: x.id, stripe.Charge.all(count=100, customer = customer.id).data)
    except InvalidRequestError as e:
        raise Http404(e)
    
    try:
        charge = stripe.Charge.retrieve(id=charge_id)
    except InvalidRequestError as e:
        raise Http404(e)
            
    if not charge.id in charge_ids:
        raise Http403("You do not have permission to view this receipt.")
    
    pdf_path = get_or_create_receipt_pdf(charge, employer.name)
    pdf_name = pdf_path.split("/")[-1]
    
    mimetype = "application/pdf"
    response = HttpResponse(file(pdf_path, "rb").read(), mimetype=mimetype)
    response["Content-Disposition"] = 'inline; filename="%s"' % pdf_name
    return response


@user_passes_test(is_recruiter)
def receipts_view(request):
    customer = request.META.get('customer', None)
    employer = request.user.recruiter.employer
        
    charges = stripe.Charge.all(count=100, customer = customer.id).data

    pdf_name = "Umeqo %s Charges.pdf" % (employer)
    path = "%semployer/receipts/" % (s.MEDIA_ROOT)
    pdf_path = "%s%s" % (path, pdf_name)
    
    output = PdfFileWriter()
    for charge in charges:
        receipt_path = get_or_create_receipt_pdf(charge, employer.name)
        receipt_file = open(receipt_path, "rb")
        output.addPage(PdfFileReader(receipt_file).getPage(0))
    if not os.path.exists(path):
        os.makedirs(path)
    outputStream = file(pdf_path, "wb")
    output.write(outputStream)
    outputStream.close()
    receipt_file.close()
    
    mimetype = "application/pdf"
    response = HttpResponse(file(pdf_path, "rb").read(), mimetype=mimetype)
    response["Content-Disposition"] = 'inline; filename="%s"' % pdf_name
    return response


@user_passes_test(is_recruiter)
@render_to("subscription_cancel.html")
def subscription_cancel(request, extra_context=None):
    context = {}
    customer = request.META['customer']
    if request.method == "POST":
        customer.cancel_subscription(at_period_end=True)
        return redirect("%s%s" % (reverse("employer_account"), "?msg=subscription-cancelled&tab=subscription"))
    else:
        context['customer'] = customer
        context['premium_subscription_uids'] = map(lambda x: x[1], s.SUBSCRIPTION_UIDS['premium'].values())
        context['feature_template'] = "subscription_features_%s.html" % get_subscription_type(customer.subscription.plan.id)
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