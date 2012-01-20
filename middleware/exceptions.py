import logging
import sys

from django.http import Http404

from core.http import Http500, Http403, Http400
from core.views import handle_500, handle_404, handle_403, handle_400
from sentry.client.models import get_client

class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if type(exception)==Http500:
            message_id = get_client().create_from_exception(sys.exc_info(), request=request, level=logging.ERROR, logger='http500')
            request.sentry = {
                'id': message_id,
            }
            return handle_500(request, str(exception))
        elif type(exception)==Http404:
            message_id = get_client().create_from_exception(sys.exc_info(), request=request, level=logging.INFO, logger='http404')
            request.sentry = {
                'id': message_id,
            }
            return handle_404(request, str(exception))
        elif type(exception)==Http403:
            message_id = get_client().create_from_exception(sys.exc_info(), request=request, level=logging.INFO, logger='http403')
            request.sentry = {
                'id': message_id,
            }
            return handle_403(request, str(exception))
        elif type(exception)==Http400:
            message_id = get_client().create_from_exception(sys.exc_info(), request=request, level=logging.WARNING, logger='http400')
            request.sentry = {
                'id': message_id,
            }
            return handle_400(request, str(exception))
        return None