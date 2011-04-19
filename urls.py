"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.simple import direct_to_template

admin.autodiscover()

import haystack
haystack.autodiscover()

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^notifications/', include('notification.urls')),
    url(r'^logout/$', auth_views.logout_then_login, {'login_url':'/?action=logged-out'}, name='logout'),
    url(r'^password/change/$', auth_views.password_change, {'template_name' : 'password_change_form.html'}, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name' : 'password_change_done.html'}, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, {'template_name' : 'password_reset_form.html', 'email_template_name': 'password_reset_email.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name' : 'password_reset_confirm.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name' : 'password_reset_complete.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, {'template_name' : 'password_reset_done.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset_done'),
)

urlpatterns += patterns('core.views',
    (r'^$', 'home', {'extra_context': {'login_form':AuthenticationForm}}, 'home'),
    (r'^about/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'about.html' }, 'about'),
    (r'^blog/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'blog.html' }, 'blog'),
    (r'^enable-javascript/$', direct_to_template, { 'template' : 'enable_javascript.html' }, 'enable_javascript'),
    (r'^browser-not-supported/$', direct_to_template, { 'template' : 'browser_not_supported.html' }, 'browser_not_supported'),
)

urlpatterns += patterns('help.views',
    (r'^help/$', 'help', {'extra_context': {'login_form':AuthenticationForm}}, 'help'),
)

urlpatterns += patterns('contact_form.views',
    (r'^contact_us_dialog/$', 'contact_us_dialog', {}, 'contact_us_dialog'),
)

urlpatterns += patterns('registration.views',
    (r'^login/', 'login', {}, 'login'),
    (r'^student/activation/(?P<activation_key>\w+)/$', 'activate_user', {}, 'student_activation'),
)

urlpatterns += patterns('student.views',
    # Student Registration
    (r'^student/registration/$', 'student_registration', {'extra_context': {'login_form':AuthenticationForm}}, "student_registration"),
    (r'^student/registration/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'registration_complete.html' }, 'student_registration_complete'),
    (r'^student/activation/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'registration/activation_complete.html' }, 'registration_activation_complete'),
    (r'^student/registration/closed/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'registration/registration_closed.html' }, 'student_registration_closed'),
    # Student Profile Management
    (r'^student/edit-profile/$', 'student_edit_profile', {}, "student_edit_profile"),
    (r'^student/create-profile/$', 'student_create_profile', {}, "student_create_profile"),
    (r'^student/profile-form-info/$', 'student_profile_form_info', {}, 'student_profile_form_info'),
    (r'^student/create-campus-organization/$', 'student_create_campus_organization', {}, 'student_create_campus_organization'),
    (r'^student/create-language/$', 'student_create_language', {}, 'student_create_language'),
    (r'^student/update-resume/$', 'student_update_resume', {}, 'student_update_resume'),
    # Student Account Settings
    (r'^student/account-settings/$', 'student_account_settings', {}, "student_account_settings"),   
    # Student Employer Subscriptions
    (r'^student/employer-subscriptions/$', 'student_employer_subscriptions', {}, 'student_employer_subscriptions'),
    (r'^student/suggested-employers-list/$', 'student_suggested_employers_list', {}, 'student_suggested_employers_list'),
    # Student Events
    (r'^student/events/$', 'student_events', {}, 'student_events'),
    # Student Invitations
    (r'^student/invitations/$', 'student_invitations', {}, 'student_invitations'),
    # Student Home
    (r'^student/(?P<username>\w+)/$', 'student_home', {}, "student_home"),    
)

urlpatterns += patterns('employer.views',
    # Employer Registration
    (r'^employer/register/$', 'employer_register', {'extra_context': {'login_form':AuthenticationForm}}, 'employer_register'),
    # Employer Account Settings
    (r'^employer/account-settings/$', 'employer_account_settings', {}, 'employer_account_settings'), 
    # Employer Student Default Filtering Parameters
    (r'^employer/setup-default-filtering-parameters', 'employer_setup_default_filtering_parameters', {}, 'employer_setup_default_filtering_parameters'),
    # Employer Student Filtering
    (r'^employer/add-to-resume-book/(?P<student_id>\d+)/$', 'employer_add_to_resume_book', {}, 'employer_add_to_resume_book'),
    (r'^employer/filtering/$', 'employer_filtering', {}, 'employer_filtering'),
    # Employer Events
    (r'^employer/events/$', 'employer_events', {}, 'employer_events'),
    (r'^employer/events/summary/(?P<id>\d+)/$', 'employer_event_summary', {}, 'employer_event_summary'),
    (r'^employer/events/(?P<id>\d+)/$', 'employer_event', {}, 'employer_event'),
    (r'^employer/events/new/$', 'employer_new_event', {}, 'employer_new_event'),
    # Employer Invitations
    (r'^employer/invitations/$', 'employer_invitations', {}, 'employer_invitations'),
    # Employer Home
    (r'^employer/(?P<username>\w+)/$', 'employer_home', {}, 'employer_home'),
)

urlpatterns += patterns('core.ajax_views',              
    (r'^get_course_info/$', 'get_course_info'),
    (r'^check_email_availability/$', 'check_email_availability'),
    (r'^check_email_existence/$', 'check_email_existence'),
    (r'^check_username_existence/$', 'check_username_existence'),
    (r'^resume_info/$', 'resume_info'),
    (r'^check_password/$', 'check_password'),
    (r'^check-campus-organization-uniqueness/$', 'check_campus_organization_uniqueness'),
    (r'^check-language-uniqueness/$', 'check_language_uniqueness'),
    (r'^check-website/$', 'check_website')
)