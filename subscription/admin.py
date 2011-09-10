from django import forms
from django.contrib import admin
from django.utils.html import conditional_escape as esc

from models import Subscription, EmployerSubscription, Transaction

def _pricing(sub): return sub.get_pricing_display()
def _trial(sub): return sub.get_trial_display()

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', _pricing, _trial)
admin.site.register(Subscription, SubscriptionAdmin)

def _subscription(trans):
    return u'<a href="/admin/subscription/subscription/%d/">%s</a>' % (
        trans.subscription.pk, esc(trans.subscription) )
_subscription.allow_tags = True

def _employer(trans):
    return u'<a href="/admin/employer/employer/%d/">%s</a>' % (
        trans.employer.pk, esc(trans.employer) )
_employer.allow_tags = True

def _ipn(trans):
    return u'<a href="/admin/ipn/paypalipn/%d/">#%s</a>' % (
        trans.ipn.pk, trans.ipn.pk )
_ipn.allow_tags = True

class EmployerSubscriptionAdminForm(forms.ModelForm):
    class Meta:
        model = EmployerSubscription
    fix_group_membership = forms.fields.BooleanField(required=False)
    extend_subscription = forms.fields.BooleanField(required=False)

class EmployerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ( '__unicode__', _employer, _subscription, 'expires' )
    list_display_links = ( '__unicode__', )
    list_filter = ('subscription', )
    date_hierarchy = 'expires'
    form = EmployerSubscriptionAdminForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['extend_subscription']:
            obj.extend()
        obj.save()

    # action for Django-SVN or django-batch-admin app
    actions = ( 'extend', )

    def extend(self, request, queryset):
        for us in queryset.all(): us.extend()
    extend.short_description = 'Extend subscription'

admin.site.register(EmployerSubscription, EmployerSubscriptionAdmin)

class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ("employer", 'timestamp', 'person', 'email', 'amount', 'payment')
    list_filter = ('person', 'payment')
admin.site.register(Transaction, TransactionAdmin)
