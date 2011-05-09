"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

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
        if request.method == "POST":
            redirect_to = request.POST.get(redirect_field_name, '')
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user_cache = authenticate(username = username, password=password)
                if user_cache is None:
                    return HttpResponse(simplejson.dumps({"valid":False, "reason":"invalid"}), mimetype="application/json")
                elif not user_cache.is_active:
                    return HttpResponse(simplejson.dumps({"valid":False, "reason":"inactive"}), mimetype="application/json")
                else:
                    if not request.session.test_cookie_worked():
                        return HttpResponse(simplejson.dumps({"valid":False, "reason":"cookies_disabled"}), mimetype="application/json")
                    auth_login(request, user_cache)
                    return HttpResponse(simplejson.dumps({"valid":True, "url":modify_redirect(request, redirect_to)}), mimetype="application/json")
    return redirect("home")


def activate_user(request, 
                  backend = RegistrationBackend(),
                  template_name='invalid_activation_link.html',
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
        
    kwargs.update(extra_context or {})
    return render_to_response(template_name,
                              kwargs,
                              context_instance=RequestContext(request))