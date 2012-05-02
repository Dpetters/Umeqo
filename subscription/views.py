import os
import stripe


from django.http import HttpResponse, Http404
from django.conf import settings as s
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from pyPdf import PdfFileWriter, PdfFileReader
from stripe import InvalidRequestError

from core.decorators import render_to
from core.email import send_html_mail
from core.http import Http403, Http400
from core.templatetags.filters import format_unix_time
from employer.decorators import is_recruiter
from subscription.forms import CheckoutForm, ChangeBillingForm, CardForm, SubscriptionChangeForm, AccountRequestForm
from subscription.utils import get_subscription_type
from subscription.view_helpers import create_charge_page


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
    stripe.api_key = s.STRIPE_SECRET
    context = {'plan':plan}
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
    try:
        plan_uids = map(lambda x: x[1], s.SUBSCRIPTION_UIDS[plan].values()) 
    except KeyError as e:
        raise Http403("You cannot upgrade to the %s plan." % plan)
    if customer.subscription and customer.subscription.plan.id in plan_uids:
        return redirect(reverse("subscription_change"))
    if request.method == 'POST':
        form = form_class(plan, request.POST)
        if form.is_valid():
            token = form.cleaned_data['stripe_token']
            card = None
            if token:
                card = token
            billing_cycle = form.cleaned_data['billing_cycle']
            customer.update_subscription(plan=s.SUBSCRIPTION_UIDS[plan][billing_cycle][1], card=card)
            return redirect(reverse('employer_account'))
    else:
        form = form_class(plan)
        context['customer'] = customer
    context['form'] = form
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
@render_to("subscription_billing_cycle_change.html")
def subscription_billing_cycle_change(request, form_class=ChangeBillingForm, extra_context=None):
    stripe.api_key = s.STRIPE_SECRET
    context = {}
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
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
            return redirect(reverse('employer_account'))
    else:
        form = form_class(plan, customer.subscription.plan.interval)
        context['customer'] = customer
    context['form'] = form
    context.update(extra_context or {})
    return context


@user_passes_test(is_recruiter)
def subscription_billing_cycle_price(request, extra_context=None):
    if not request.POST.has_key('billing_cycle'):
        raise Http400("Request POST is missing student_ids.")
    
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
    #current_billing_cycle = 
    return HttpResponse()


@user_passes_test(is_recruiter)
def receipt_view(request, charge_id):
    stripe.api_key = s.STRIPE_SECRET
    
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
    
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
    
    pdf_name = "Umeqo_Charge_%s_%s.pdf" % (format_unix_time(charge.created).replace("/", "-"), charge_id)
    path = "%semployer/receipts/" % (s.MEDIA_ROOT)
    pdf_path = "%s%s" % (path, pdf_name)
    if not os.path.exists(pdf_path):
        output = PdfFileWriter()
        output.addPage(PdfFileReader(create_charge_page(charge, request.user.recruiter.employer)).getPage(0))
        if not os.path.exists(path):
            os.makedirs(path)
        outputStream = file(pdf_path, "wb")
        output.write(outputStream)
        outputStream.close()
    mimetype = "application/pdf"
    response = HttpResponse(file(pdf_path, "rb").read(), mimetype=mimetype)
    response["Content-Disposition"] = 'inline; filename="%s"' % pdf_name
    return response

@user_passes_test(is_recruiter)
def receipts_view(request):
    stripe.api_key = s.STRIPE_SECRET
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
    charges = stripe.Charge.all(count=100, customer = customer.id).data
    employer = request.user.recruiter.employer
    pdf_name = "Umeqo %s Charges.pdf" % (employer)
    path = "%semployer/receipts/" % (s.MEDIA_ROOT)
    pdf_path = "%s%s" % (path, pdf_name)
    
    output = PdfFileWriter()
    for charge in charges:
        output.addPage(PdfFileReader(create_charge_page(charge, request.user.recruiter.employer)).getPage(0))
    if not os.path.exists(path):
        os.makedirs(path)
    outputStream = file(pdf_path, "wb")
    output.write(outputStream)
    outputStream.close()
    
    mimetype = "application/pdf"
    response = HttpResponse(file(pdf_path, "rb").read(), mimetype=mimetype)
    response["Content-Disposition"] = 'inline; filename="%s"' % pdf_name
    return response

@user_passes_test(is_recruiter)
@render_to("subscription_cancel.html")
def subscription_cancel(request, extra_context=None):
    context = {}
    stripe.api_key = s.STRIPE_SECRET
    employer = request.user.recruiter.employer
    customer = employer.get_customer()
    if request.method == "POST":
        customer.cancel_subscription(at_period_end=True)
        return redirect("%s%s" % (reverse("employer_account"), "?msg=subscription-cancelled&tab=subscription"))
    else:
        context['premium_subscription_uids'] = map(lambda x: x[1], s.SUBSCRIPTION_UIDS['premium'].values())
        context['customer'] = customer
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