"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.shortcuts import render_to_response
from django.template import RequestContext

def enable_javascript(request,
                      template_name="enable_javascript.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))


def browser_not_supported(request,
                          template_name="browser_not_supported.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))


def about(request,
          template_name="about.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))


def blog(request,
         template_name="blog.html"):
    return render_to_response(template_name, context_instance=RequestContext(request))