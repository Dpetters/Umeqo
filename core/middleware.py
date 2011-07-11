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
            message     = getattr(exception, "message", ""),
            url         = request.build_absolute_uri(),
            server_name = server_name,
            traceback   = tb_text,
        ) 
        logger.error(exception_info)
      
   
class SetRemoteAddrMiddleware(object):
    def process_request(self, request):
        if not request.META.has_key('REMOTE_ADDR'):
            try:
                request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
            except:
                request.META['REMOTE_ADDR'] = '1.1.1.1' # This will place a valid IP in REMOTE_ADDR but this shouldn't happen