from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings as s
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import simplejson
from django.template.loader import render_to_string

from core.email import send_html_mail
from employer.models import Recruiter
from core.decorators import is_recruiter, render_to
from subscription.models import Subscription, EmployerSubscription
from subscription.forms import SubscriptionCancelForm, SubscriptionForm, subscription_templates

@render_to("subscription_transaction_dialog.html")
def subscription_dialog(request, extra_context=None):
    if request.method=="POST":
        if request.POST.has_key("action") and request.POST.has_key("subscription_type"):
            action = request.POST['action']
            if action not in subscription_templates:
                return HttpResponseBadRequest("Subscription transaction type must be one of the following: %s" % (subscription_templates.keys()))
            subscription_type = request.POST['subscription_type']
        else:
            return HttpResponseBadRequest("Subscription transaction type or action is missing.")
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
            subject = "[sales] %s subscription request" % subscription_type
            subscription_request_context = {'name': form.cleaned_data['name'], 'employer':form.cleaned_data['employer'], 'email': form.cleaned_data['email'], 'body': form.cleaned_data['body']}
            html_body = render_to_string('subscription_body_request.html', subscription_request_context)
            send_html_mail(subject, html_body, recipients)
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
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
        if request.user.is_authenticated():
            initial['name'] = "%s %s" % (request.user.first_name, request.user.last_name,)
            initial['email'] = request.user.email
            initial['employer'] = request.user.recruiter.employer
        
        body_context = {'subscription_type':subscription_type}
        if is_recruiter(request.user):
            body_context['employer'] = request.user.recruiter.employer
        initial['body'] = render_to_string(subscription_templates[action], body_context)
        
        context = {}
        if type=="cancel":
            context['form'] = SubscriptionCancelForm(initial=initial)
        else:
            context['form'] = SubscriptionForm(initial=initial)
        
        context.update(extra_context or {})
        return context
             
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
        context = {'user':request.user }
        free_trial = Subscription.objects.get(name="Free Trial")
        try:
            es = request.user.recruiter.employer.employersubscription
            if es.subscription == free_trial:
                context['ft_text'] = "Extend Subscription"
                context['ft_class'] = "open_sd_link extend"
                context['ft_action'] = "extend"
                if es.expired:
                    context['a_text'] = "Upgrade"
                    context['a_cancel'] = "open_sd_link upgrade"
                    context['a_action'] = "upgrade"
                    context['a_dialog_title'] = "Upgrade Subscription"
                else:
                    context['ft_text'] = "Cancel Subscription"
                    context['ft_class'] = "open_sd_link cancel"
                    context['ft_action'] = "cancel"
            else:
                context['a_text'] = "Cancel Subscription"
                context['a_class'] = "open_sd_link cancel"
                context['a_action'] = "cancel"
                context['a_dialog_title'] = "Cancel Subscription"
        except EmployerSubscription.DoesNotExist:
            context = {'ft_class':'open_ftid_link', 'a_dialog_title':"Subscribe to Umeqo", 'a_action': 'subscribe', 'a_class':"open_sd_link subscribe"}
    else:
        context = {'ft_class':'open_ftid_link', 'a_dialog_title':"Subscribe to Umeqo", 'a_action': 'subscribe', 'a_class':"open_sd_link subscribe"}
    context.update(extra_context or {})
    return context