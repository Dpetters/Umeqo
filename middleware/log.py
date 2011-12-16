import traceback
import socket
import logging

class LogMiddleware(object):
    def process_exception(self, request, exception):
        
        logger = logging.getLogger("django.request")
        
        server_name = socket.gethostname()
        tb_text     = traceback.format_exc()
        class_name  = exception.__class__.__name__

        exception_info = dict(
            class_name  = class_name,
            message     = str(exception),
            url         = request.build_absolute_uri(),
            server_name = server_name,
            traceback   = tb_text,
        ) 
        logger.error(exception_info)