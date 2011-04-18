from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login

from registration.backend import RegistrationBackend
from registration.view_helpers import modify_redirect

def login(request,
        redirect_field_name = REDIRECT_FIELD_NAME,
        template_name='homepage.html'):

    if request.is_ajax():
        redirect_to = request.REQUEST.get(redirect_field_name, '')
            
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user_cache = authenticate(username = username, password=password)
                if user_cache is None:
                    return HttpResponse(simplejson.dumps("invalid"), mimetype="application/json")
                elif not user_cache.is_active:
                    return HttpResponse(simplejson.dumps("inactive"), mimetype="application/json")
                else:
                    if not request.session.test_cookie_worked():
                        return HttpResponse(simplejson.dumps("cookies_disabled"), mimetype="application/json")
                    auth_login(request, user_cache)
                    return HttpResponse(simplejson.dumps(modify_redirect(request, redirect_to)), mimetype="application/json")
    return redirect("home")
            
def activate_user(request, 
                  backend = RegistrationBackend(),
                  template_name='registration/invalid_activation_link.html',
                  success_url=None, 
                  extra_context=None, 
                  **kwargs):

    account = backend.activate(request, **kwargs)

    if account:
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)
