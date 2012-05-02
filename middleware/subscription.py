from django.conf import settings as s

from employer.decorators import is_recruiter


def has_at_least_premium(customer):
    subscription = customer.subscription
    if subscription:
        return subscription.plan.id in map(lambda x: x[1], s.SUBSCRIPTION_UIDS['premium'].values()) and subscription.status != "cancelled"
    return False
    
    
class SubscriptionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if is_recruiter(request.user):
            print "Processing view"
            customer = request.user.recruiter.employer.get_customer()
            request.META['customer'] = customer
            has_at_least_premium_var = has_at_least_premium(customer)
            request.META['has_at_least_premium'] = has_at_least_premium_var
            request.META['can_upgrade'] = not has_at_least_premium_var
            print "Done procesing view"