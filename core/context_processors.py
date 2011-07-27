def next(request):
    return {'login_next': request.GET.get('next', '/')} if 'next' in request.GET else {}

def get_current_path(request):
    return {
       'current_path': request.get_full_path().split("?")[0]
     }