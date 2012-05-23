from django.conf import settings as s
from django.contrib.staticfiles.views import serve

from debug_toolbar.views import debug_media
from employer.decorators import is_recruiter


def has_at_least_premium(customer):
    if customer:
        subscription = customer.subscription
        if subscription:
            return subscription.plan.id in map(lambda x: x[1], s.SUBSCRIPTION_UIDS['premium'].values()) and subscription.status != "cancelled"
    return False
    
    
class SubscriptionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not view_func == serve and not view_func == debug_media and is_recruiter(request.user):
            customer = request.user.recruiter.employer.get_customer()
            request.META['customer'] = customer
            has_at_least_premium_var = has_at_least_premium(customer)
            request.META['has_at_least_premium'] = has_at_least_premium_var
            request.META['can_upgrade'] = not has_at_least_premium_var