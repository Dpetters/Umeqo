from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings as s
from django.utils import simplejson
from django.template.loader import render_to_string

from core.email import send_html_mail
from core.decorators import is_recruiter, render_to
from core.http import Http403
from subscription.choices import EMPLOYER_SIZE_CHOICES
from subscription.models import EmployerSubscription
from subscription.forms import SubscriptionForm, subscription_templates

@render_to("subscription_transaction_dialog.html")
def subscription_transaction_dialog(request, form_class = SubscriptionForm, extra_context=None):
    if not request.is_ajax():
        raise Http403
    if request.method=="POST":
        if not request.POST.has_key("action"):
            return HttpResponseBadRequest("Action is missing from the request POST.")
        action = request.POST['action']
        if action not in subscription_templates:
            return HttpResponseBadRequest("Subscription transaction type must be one of the following: %s" % (subscription_templates.keys()))
        form = form_class(data = request.POST, user=request.user)
        if form.is_valid():
            if is_recruiter(request.user):
                employer = request.user.recruiter.employer
                employer.size = form.cleaned_data['employer_size']
                employer.save()
            data = []
            recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
            subject = "[Umeqo Sales] %s wants to %s" % (form.cleaned_data['employer_name'], action)
            subscription_email_context = {'form':form}
            html_body = render_to_string('subscription_body_request.html', subscription_email_context)
            send_html_mail(subject, html_body, recipients)
        else:
            data = {'errors':form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        if not request.GET.has_key("action"):
            raise Http403("Action is missing from the request POST.")
        action = request.GET['action']
        if action not in subscription_templates:
            raise Http403("Subscription transaction type must be one of the following: %s" % (subscription_templates.keys()))
        initial = {}
        initial['message_body'] = render_to_string(subscription_templates[action], {})
        context = {'form':form_class(initial=initial, user=request.user)}
        context.update(extra_context or {})
        return context
             
@render_to("event_subscription_info_dialog.html")
def free_subscription_info_dialog(request, extra_context=None):
    context = {}
    context.update(extra_context or {})
    return context

@render_to("subscription_list.html")
def subscription_list(request, extra_context=None):
    context = {}
    subscription=None
    if request.user.is_authenticated() and is_recruiter(request.user):
        context['user'] = request.user
        employer = request.user.recruiter.employer
        try:
            subscription = employer.employersubscription
        except EmployerSubscription.DoesNotExist:
            subscription = None
    
    if subscription:
        if subscription.expired():
            if subscription.event_subscription():
                context['free_subscription_text'] = "Subscription Expired"
                context['free_subscription_class'] = 'open_free_subscription_info_dialog_link'
                context['transaction_dialog_title'] = "Subscribe to Umeqo" 
                context['paid_subscription_class'] = "subscribe"
            else:
                context['paid_subscription_button_text'] = "Extend Subscription"
                context['transaction_dialog_title'] = "Extend Subscription"
                context['paid_subscription_class'] = "extend"
                context['paid_subscription_action'] = "extend"
                context['paid_subscription_text'] = "Subscription Expired"
        else:
            if subscription.event_subscription():
                context['paid_subscription_button_text'] = "Upgrade to Annual Plan"
                context['transaction_dialog_title'] = "Upgrade to Annual Subscription"
                context['paid_subscription_class'] = "upgrade"
                context['paid_subscription_action'] = "upgrade"
                context['free_subscription_text'] = "Subscribed"
            else:
                context['paid_subscription_button_text'] = "Extend Subscription"
                context['transaction_dialog_title'] = "Extend Subscription"
                context['paid_subscription_class'] = "extend"
                context['paid_subscription_action'] = "extend"
                context['paid_subscription_text'] = "Subscribed"
    else:
        context['free_subscription_class'] = 'open_free_subscription_info_dialog_link'
        context['transaction_dialog_title'] = "Subscribe to Umeqo" 
        context['paid_subscription_class'] = "subscribe"
    context.update(extra_context or {})
    return context