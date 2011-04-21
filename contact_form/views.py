"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from contact_form.forms import AkismetContactForm

def contact_us_dialog(request,
                      template_name='contact_dialog.html',
                      form_class=AkismetContactForm,
                      fail_silently=False,
                      extra_context=None):
    if request.is_ajax():
        if request.method == 'POST':
            form = form_class(data=request.POST, request=request)
            if form.is_valid():
                form.save(fail_silently=fail_silently)
                return HttpResponse(simplejson.dumps({"valid":True}))
            return HttpResponse(simplejson.dumps({"valid":False}))
        else:
            form = form_class(request=request)
    
        context = {
                'contact_form': form,
                }
        context.update(extra_context or {}) 
        return render_to_response(template_name,
                                  context,
                                  context_instance=RequestContext(request))
    return redirect('home')