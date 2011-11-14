from datetime import date

from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings as s
from django.utils import simplejson
from django.template.loader import render_to_string

from core.email import send_html_mail
from core.decorators import is_recruiter, render_to
from subscription.models import EmployerSubscription
from subscription.forms import SubscriptionForm, subscription_templates

@render_to("subscription_transaction_dialog.html")
def subscription_dialog(request, form_class = SubscriptionForm, extra_context=None):
    if request.is_ajax():
        if request.method=="POST":
            if request.POST.has_key("action") and request.POST.has_key("subscription_type"):
                action = request.POST['action']
                if action not in subscription_templates:
                    return HttpResponseBadRequest("Subscription transaction type must be one of the following: %s" % (subscription_templates.keys()))
                subscription_type = request.POST['subscription_type']
            else:
                return HttpResponseBadRequest("Subscription transaction type or action is missing.")
            
            form = form_class(data = request.POST, user=request.user)
            
            if form.is_valid():
                data = []
                recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                subject = "[sales] %s subscription request" % subscription_type
                subscription_request_context = {'name': form.cleaned_data['name'], 'employer':form.cleaned_data['employer'], 'email': form.cleaned_data['email'], 'body': form.cleaned_data['body']}
                html_body = render_to_string('subscription_body_request.html', subscription_request_context)
                send_html_mail(subject, html_body, recipients)
            else:
                data = {'error':form.errors}
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        else:
            if request.GET.has_key("action") and request.GET.has_key("subscription_type"):
                action = request.GET['action']
                if action not in subscription_templates:
                    return HttpResponseBadRequest("Subscription transaction type must be one of the following: %s" % (subscription_templates.keys()))
                subscription_type = request.GET['subscription_type']
            else:
                return HttpResponseBadRequest("Subscription transaction type or action is missing.")
            
            initial = {}
            if is_recruiter(request.user):
                initial['name'] = "%s %s" % (request.user.first_name, request.user.last_name,)
                initial['email'] = request.user.email
                initial['employer'] = request.user.recruiter.employer
            
            body_context = {'subscription_type':subscription_type}
            initial['body'] = render_to_string(subscription_templates[action], body_context)
            
            context = {'form':form_class(initial=initial, user=request.user)}
            
            context.update(extra_context or {})
            return context
    else:
        return HttpResponseBadRequest("Request must be ajax.")
             
@render_to("free_trial_info_dialog.html")
def free_trial_info_dialog(request, extra_context=None):
    context = {}
    context.update(extra_context or {})
    return context

@render_to("subscription_list.html")
def subscription_list(request, extra_context=None):
    if request.user.is_authenticated() and is_recruiter(request.user):
        context = {'user':request.user}
        employer = request.user.recruiter.employer
        try:
            es = employer.employersubscription
        except EmployerSubscription.DoesNotExist:
            pass
        else:
            if es.expired() or es.expires < date.today():
                context['annual_button'] = "Extend Subscription"
                context['annual_dialog'] = "Extend Subscription"
                context['annual_class'] = "open_sd_link extend"
                context['annual_action'] = "extend"
                context['annual_text'] = "Subscription Expired"
            else:
                context['annual_button'] = "Extend Subscription"
                context['annual_dialog'] = "Extend Subscription"
                context['annual_class'] = "open_sd_link extend"
                context['annual_action'] = "extend"
                context['annual_text'] = "Subscribed"

    else:
        context = {'free_trial_class':'open_ftid_link',
                   'annual_button':"Contact Us",
                   'annual_dialog':"Subscribe to Umeqo", 
                   'annual_action': 'subscribe', 
                   'annual_class':"open_sd_link subscribe",
                   'annual_text':"Contact Us For Pricing"}
    context.update(extra_context or {})
    return context