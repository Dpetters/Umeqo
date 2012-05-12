from core.http import Http403


def is_recruiter(user):
    return hasattr(user, "recruiter")


class has_at_least_premium(object):
    def __init__(self, orig_func):
        self.orig_func = orig_func
    
    def __call__(self, request, *args, **kwargs):
        if not request.META['has_at_least_premium']:
            raise Http403("You need to have a Umeqo Premium subscription to perform this action.")
        return self.orig_func(request, *args, **kwargs)