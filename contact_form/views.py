"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from contact_form.forms import AkismetContactForm

def contact_us_dialog(request,
                      template_name='contact_dialog.html',
                      form_class=AkismetContactForm,
                      login_required=False, #@UnusedVariable
                      fail_silently=False):

    if request.method == 'POST':
        contact_form = form_class(data=request.POST, request=request)
        if contact_form.is_valid():
            contact_form.save(fail_silently=fail_silently)
            return HttpResponse(simplejson.dumps({"valid":True}))
        return HttpResponse(simplejson.dumps({"valid":False}))
    else:
        contact_form = form_class(request=request)

    data = {
            'contact_form': contact_form,
            }

    return render_to_response(template_name, data, context_instance=RequestContext(request))