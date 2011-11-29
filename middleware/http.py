from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.template import RequestContext
from django.template import loader

class HttpResponseNotAllowedMiddleware(object): 
    def process_response(self, request, response): 
        if isinstance(response, HttpResponseNotAllowed): 
            context = RequestContext(request) 
            response.content = loader.render_to_string("405.html", context_instance=context) 
        return response

class Http403Middleware(object):
    """Replaces vanilla django.http.HttpResponseForbidden() responses
    with a rendering of 403.html
    """
    def process_response(self, request, response):
        # If the response object is a vanilla 403 constructed with
        # django.http.HttpResponseForbidden() then call our custom 403 view
        # function
        if isinstance(response, HttpResponseForbidden) and set(dir(response)) == set(dir(HttpResponseForbidden())):
            t = loader.get_template('403.html')
            template_values = {}
            template_values['request'] = request
            return HttpResponseForbidden(t.render(RequestContext(request, template_values)))
        return response