"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.shortcuts import render_to_response
from django.template import RequestContext

def enable_javascript(request):
    return render_to_response("enable_javascript.html", context_instance=RequestContext(request))

def browser_not_supported(request):
    return render_to_response("browser_not_supported.html", context_instance=RequestContext(request))

def about(request):
    pass


def faq(request):
    pass


def blog(request):
    pass


def advertise(request):
    pass