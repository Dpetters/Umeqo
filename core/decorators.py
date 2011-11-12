from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden

from subscription.models import EmployerSubscription, Subscription

class agreed_to_terms(object):
    def __init__(self, orig_func):
        self.orig_func = orig_func
    
    @property
    def __name__(self):
        return self.__class__.__name__
    
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.is_staff or request.user.userattributes.agreed_to_terms:
            return self.orig_func(request, *args, **kwargs)
        return redirect(reverse("terms_of_service"))
    
class has_any_subscription(object):
    def __init__(self, orig_func):
        self.orig_func = orig_func
    
    def __call__(self, request, *args, **kwargs):
        if is_recruiter(request.user):
            try:
                s = request.user.recruiter.employer.employersubscription
                if not s.expired():
                    return self.orig_func(request, *args, **kwargs)
            except EmployerSubscription.DoesNotExist:
                pass
            if request.is_ajax():
                return HttpResponseForbidden("You must have an annual subscription to do that.")
            return redirect(reverse("subscription_list"))
        return self.orig_func(request, *args, **kwargs)

class has_annual_subscription(object):
    def __init__(self, orig_func):
        self.orig_func = orig_func
    
    def __call__(self, request, *args, **kwargs):
        if is_recruiter(request.user):
            return self.orig_func(request, *args, **kwargs)
            """
            if request.is_ajax():
                return HttpResponseForbidden("You must have an annual subscription to do that.")
            """
            return redirect(reverse("subscription_list"))
        return self.orig_func(request, *args, **kwargs)

def is_superuser(user):
    return user.is_superuser

def is_campus_org(user):
    return hasattr(user, "campusorg")
    
def is_student(user):
    return hasattr(user, "student")
    
def is_recruiter(user):
    return hasattr(user, "recruiter")

def is_campus_org_or_recruiter(user):
    return hasattr(user, "recruiter") or hasattr(user, "campusorg")

def is_student_or_recruiter(user):
    return hasattr(user, "recruiter") or hasattr(user, "student")
#
try:
    from functools import wraps
except ImportError: 
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner

def render_to(template=None, mimetype=None):
    """
    Decorator for Django views that sends returned dict to render_to_response 
    function.

    Template name can be decorator parameter or TEMPLATE item in returned 
    dictionary.  RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
     - template: template name to use
     - mimetype: content type to send in response headers

    Examples:
    # 1. Template name in decorator parameters

    @render_to('template.html')
    def foo(request):
        bar = Bar.object.all()  
        return {'bar': bar}

    # equals to 
    def foo(request):
        bar = Bar.object.all()  
        return render_to_response('template.html', 
                                  {'bar': bar}, 
                                  context_instance=RequestContext(request))


    # 2. Template name as TEMPLATE item value in return dictionary.
         if TEMPLATE is given then its value will have higher priority 
         than render_to argument.

    @render_to()
    def foo(request, category):
        template_name = '%s.html' % category
        return {'bar': bar, 'TEMPLATE': template_name}
    
    #equals to
    def foo(request, category):
        template_name = '%s.html' % category
        return render_to_response(template_name, 
                                  {'bar': bar}, 
                                  context_instance=RequestContext(request))

    """
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, \
                        context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer

