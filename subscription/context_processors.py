def subscription(request):
    context = {
               'customer': request.META.get('customer', None),
               'has_at_least_premium': request.META.get('has_at_least_premium', None),
               'can_upgrade': request.META.get('can_upgrade', None)
               }
    return context
