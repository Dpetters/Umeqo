from core.decorators import is_recruiter
from core.http import Http403


class has_at_least_premium(object):
    def __init__(self, orig_func):
        self.orig_func = orig_func
    
    def __call__(self, request, *args, **kwargs):
        if is_recruiter(request.user):
            employer = request.user.recruiter.employer
            if not employer.has_at_least_premium():
                raise Http403("You need to have a Umeqo Premium subscription to perform this action.")
        return self.orig_func(request, *args, **kwargs)