def next(request):
    return {'login_next': request.GET.get('next', '/')} if 'next' in request.GET else {}