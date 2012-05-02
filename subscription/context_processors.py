def subscription(request):
    context = {
               'customer': request.META['customer'],
               'has_at_least_premium': request.META['has_at_least_premium'],
               'can_upgrade': request.META['can_upgrade']
               }
    return context
