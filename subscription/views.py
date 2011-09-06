from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import simplejson
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from employer.models import Recruiter
from core.decorators import is_recruiter, render_to
from subscription.models import _TIME_UNIT_CHOICES, Subscription, UserSubscription
from subscription.forms import SubscriptionCancelForm, SubscriptionForm, subscription_dialog_parts

@render_to("subscription_transaction_dialog.html")
def subscription_dialog(request, extra_context=None):
    if request.GET.has_key("action") and request.GET.has_key("type"):
        action = request.GET['action']
        if action in subscription_dialog_parts:
            if request.method=="POST":
                if action=="cancel":
                    form = SubscriptionCancelForm(data = request.POST)
                else:
                    form = SubscriptionForm(data = request.POST)
                if form.is_valid():
                    data = {}
                    if form.cleaned_data.has_key("new_master_recruiter"):
                        new_master = request.user.recruiter.employer.recruiter_set.get(is_master=True)           
                        data['new_master'] = new_master
                    recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                    subject = "%s request" % request.POST['type']
                    subscription_request_context = {'name': form.cleaned_data['name'], \
                                                    'email': form.cleaned_data['email'], \
                                                    'body': form.cleaned_data['body']}
                    if is_recruiter(request.user):
                        subscription_request_context['employer'] = request.user.recruiter.employer
                    body = render_to_string('subscription_request.txt', subscription_request_context)
                    message = EmailMessage(subject, body, s.DEFAULT_FROM_EMAIL, recipients)
                    message.send()
                    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
                else:
                    data = {'error':form.errors}
                return HttpResponse(simplejson.dumps(data), mimetype="application/json")
            else:
                initial = {}
                context = {'type':type}
                if request.user.is_authenticated():
                    initial['name'] = "%s %s" % (request.user.first_name, request.user.last_name,)
                    initial['email'] = request.user.email
                
                body_context = {'type':request.GET["type"]}
                if is_recruiter(request.user):
                    body_context['employer'] = request.user.recruiter.employer
                initial['body'] = render_to_string(subscription_dialog_parts[action]['template'], body_context)
                if type=="subscribe":
                    cost = Subscription.objects.get()
                    
                if type=="cancel":
                    context['form'] = SubscriptionCancelForm(initial=initial)
                else:
                    context['form'] = SubscriptionForm(initial=initial)
                context.update(extra_context or {})
                return context
        else:
            return HttpResponseBadRequest("Subscription transaction type must be one of the following: %s" % (subscription_dialog_parts.keys()))
    else:
        return HttpResponseBadRequest("Subscription transaction type or action is missing.")
             
@render_to("free_trial_info_dialog.html")
def free_trial_info_dialog(request, extra_context=None):
    context = {}
    context.update(extra_context or {})
    return context

@render_to("subscrition_cancel_done.html")
@login_required
@user_passes_test(is_recruiter, login_url = s.LOGIN_URL)
def subscription_cancel_done(request, extra_context=None):
    try:
        new_master = request.user.recruiter.employer.recruiter_set.get(is_master=True)
        context = {'new_master':new_master}
    except Recruiter.DoesNotExist:
        pass
    context.update(extra_context or {})
    return context

@render_to("subscrition_cancel.html")
@login_required
@user_passes_test(is_recruiter, login_url = s.LOGIN_URL)
def subscription_cancel(request, recruiter_id, form_class=SubscriptionCancelForm, extra_context=None):
    if recruiter_id == request.user.recruiter.id:
        own = True
    if request.method=="POST":
        data = []
        form = form_class(data = request.POST)
        if form.is_valid():
            new_master = Recruiter.objects.get(id=form.cleaned_data['recruiter'])
            new_master.is_master = True
            new_master.save()
            request.user.unsubscribe()
        else:
            data = {'errors': form.errors}
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        form = form_class(initial={'own': request.user.recruiter.employer.id})
    context = {'form':form, 'own':own}
    context.update(extra_context or {})
    return context        
    
@render_to("subscription_list.html")
def subscription_list(request, employer_type, extra_context=None):
    if not employer_type:
        return HttpResponseBadRequest("Employer type is missing.")
    context = {'employer_type':employer_type}
    if employer_type == "nonprofit":
        context['employer_type'] = "Non-Profit Employer"
        annual = Subscription.objects.get(name="Non-Profit Annual Subscription")
        quarterly = Subscription.objects.get(name="Non-Profit Quarterly Subscription")
        context['annual'] = annual
        context['quarterly'] = quarterly
    elif employer_type == "small_employer":
        context['employer_type'] = "Small Employer"
        annual = Subscription.objects.get(name="Small Employer Annual Subscription")
        quarterly = Subscription.objects.get(name="Small Employer Quarterly Subscription")
        context['annual'] = annual
        context['quarterly'] = quarterly
    elif employer_type == "medium_employer":
        context['employer_type'] = "Medium Employer"
        annual = Subscription.objects.get(name="Medium Employer Annual Subscription")
        quarterly = Subscription.objects.get(name="Medium Employer Quarterly Subscription")
        context['annual'] = annual
        context['quarterly'] = quarterly
    elif employer_type == "large_employer":
        context['employer_type'] = "Large Employer"
        annual = Subscription.objects.get(name="Large Employer Annual Subscription")
        quarterly = Subscription.objects.get(name="Large Employer Quarterly Subscription")
        context['annual'] = annual
        context['quarterly'] = quarterly
    context['annual_trial_period'] = annual.trial_period
    context['annual_trial_unit'] = dict(_TIME_UNIT_CHOICES)[annual.trial_unit]   
    context['annual_monthly_cost'] = int(annual.price_per_day() * 30)
    context['quarterly_trial_period'] = quarterly.trial_period
    context['quarterly_trial_unit'] = dict(_TIME_UNIT_CHOICES)[quarterly.trial_unit]
    context['quarterly_monthly_cost'] = int(quarterly.price_per_day() * 30)

    if request.user.is_authenticated() and is_recruiter(request.user):
        free_trial = Subscription.objects.get(name="Free Trial")
        try:
            us = request.user.usersubscription_set.get(active=True)
        except UserSubscription.DoesNotExist:
            us = None
        if us and us.subscription != free_trial:
            if us.subscription == annual:
                context['annual_button_text'] = "Cancel Subscription"
                context['annual_button_action'] = "cancel"
                context['annual_button_dialog_title'] = subscription_dialog_parts["cancel"]["title"]
                
                context['quarterly_button_text'] = "Downgrade"
                context['quarterly_button_action'] = "downgrade"
                context['annual_button_dialog_title'] = subscription_dialog_parts["downgrade"]["title"]
                                
            elif us.subscription == quarterly:
                context['annual_button_text'] = "Upgrade"
                context['annual_button_action'] = "upgrade"
                context['annual_button_dialog_title'] = subscription_dialog_parts["upgrade"]["title"]
                
                context['quarterly_button_text'] = "Cancel Subscription"
                context['quarterly_button_action'] = "cancel"
                context['quarterly_button_dialog_title'] = subscription_dialog_parts["cancel"]["title"]
        else:
            context['free_trial_button_text'] = "Cancel Subscription"
            context['free_trial_button_action'] = "cancel"
            context['free_trial_button_dialog_title'] = subscription_dialog_parts["cancel"]["title"]
            
            context['annual_button_text'] = "Upgrade"
            context['annual_button_action'] = "upgrade"
            context['annual_button_dialog_title'] = subscription_dialog_parts["upgrade"]["title"]
            
            context['quarterly_button_text'] = "Upgrade"
            context['quarterly_button_action'] = "upgrade"
            context['quarterly_button_dialog_title'] = subscription_dialog_parts["upgrade"]["title"]
    else:
        context['free_trial_button_text'] = "Learn More"
        
        context['annual_button_action'] = "subscribe"
        context['annual_button_text'] = "Contact Us"
        context['annual_button_dialog_title'] = subscription_dialog_parts["subscribe"]["title"]
                    
        context['quarterly_button_action'] = "subscribe"
        context['quarterly_button_text'] = "Contact Us"
        context['quarterly_button_dialog_title'] = subscription_dialog_parts["subscribe"]["title"]
    context.update(extra_context or {})
    return context