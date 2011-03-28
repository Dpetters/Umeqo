"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from contact_form.views import contact_us_dialog


urlpatterns = patterns('',
                       url(r'^$',
                           contact_us_dialog,
                           name='contact_form'),
                       url(r'^sent/$',
                           direct_to_template,
                           { 'template': 'contact_form/contact_form_sent.html' },
                           name='contact_form_sent'),
                       )
