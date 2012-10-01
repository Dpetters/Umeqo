from __future__ import division
from __future__ import absolute_import

from django import template
from django.http import Http404
from django.template import loader
from django.views.decorators.http import require_GET

from core.decorators import render_to

@require_GET
@render_to()
def newsletter(request, year, month):
    context = {}
    template_name = '%s/%s.html' % (year, month)
    try:
        loader.get_template(template_name)
    except template.TemplateDoesNotExist:
        raise Http404("The is no newsletter for %s of %s" % (month, year))
    context['TEMPLATE'] = template_name
    return context