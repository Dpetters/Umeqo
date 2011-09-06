from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import simplejson
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from employer.models import Recruiter
from employer import choices as employer_choices
from core.decorators import is_recruiter, render_to
from subscription.models import Subscription, UserSubscription
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
def subscription_list(request, extra_context=None):
    if request.user.is_authenticated() and is_recruiter(request.user):
        context = {}
        free_trial = Subscription.objects.get(name="Free Trial")
        try:
            us = request.user.usersubscription_set.get(active=True)
        except UserSubscription.DoesNotExist:
            us = None
        if us:
            if us.subscription == free_trial:
                context['ft_text'] = "Cancel Subscription"
                context['ft_action'] = "cancel"
                context['ft_dialog_title'] = "Cancel Suscription"
                context['ft_class'] = "open_sd_link cancel"
                
                context['a_text'] = "Upgrade"
                context['a_action'] = "upgrade"
                context['a_dialog_title'] = "Upgrade Subscription"
            else:
                context['a_text'] = "Cancel Subscription"
                context['a_action'] = "cancel"
                context['a_dialog_title'] = "Cancel Subscription"
    else:
        employer_type = None
        if request.GET.has_key("employer_type"):
            employer_type = request.GET["employer_type"]
            print employer_type
        context = {'employer_type': employer_type, 'employer_sizes':dict(employer_choices.EMPLOYER_TYPE_CHOICES)}
        if employer_type=="P":
            context['annual_monthly_cost'] = int(Subscription.objects.get(name="Non-Profit Annual Subscription").price_per_day() * 30)
        elif employer_type=="S":
            context['annual_monthly_cost'] = int(Subscription.objects.get(name="Small Employer Annual Subscription").price_per_day() * 30)
        elif employer_type=="M":
            context['annual_monthly_cost'] = int(Subscription.objects.get(name="Medium Employer Annual Subscription").price_per_day() * 30)
        elif employer_type=="L":
            context['annual_monthly_cost'] = int(Subscription.objects.get(name="Large Employer Annual Subscription").price_per_day() * 30)
    context.update(extra_context or {})
    return context