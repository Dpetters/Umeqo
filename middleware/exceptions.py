from django.http import Http404

from core.http import Http500, Http403
from core.views import handle_500, handle_404, handle_403

class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if type(exception)==Http500:
            return handle_500(request, exception)
        elif type(exception)==Http404:
            return handle_404(request, exception)
        elif type(exception)==Http403:
            return handle_403(request, exception)
        return None