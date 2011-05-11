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

from registration.forms import PasswordResetForm, SetPasswordForm

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0] }),
    )

if settings.USE_LANDING_PAGE:
    urlpatterns += patterns('',
        (r'^', 'core.views.landing_page'),
    )

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^notifications/', include('notification.urls')),
    url(r'^logout/$', auth_views.logout_then_login, {'login_url':'/?action=logged-out'}, name='logout'),
    url(r'^password/change/$', auth_views.password_change, {'template_name' : 'password_change_form.html'}, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name' : 'password_successfully_changed.html'}, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, {'password_reset_form':PasswordResetForm, 'template_name' : 'password_reset_form.html', 'email_template_name': 'password_reset_email.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'set_password_form':SetPasswordForm, 'template_name' : 'password_reset_confirm.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name' : 'password_successfully_changed.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, {'template_name' : 'password_reset_done.html', 'extra_context': {'login_form':AuthenticationForm}}, name='auth_password_reset_done'),
)

urlpatterns += patterns('core.views',
    (r'^$', 'home', {}, 'home'),
    (r'^contact-us-dialog/$', 'contact_us_dialog', {}, 'contact_us_dialog'),
    (r'^help/$', 'help', {'extra_context': {'login_form': AuthenticationForm}}, 'help'),
    (r'^about/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'about.html' }, 'about'),
    (r'^blog/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'blog.html' }, 'blog'),
    (r'^browser-configuration-not-supported/$', 'browser_configuration_not_supported', {}, 'browser_configuration_not_supported'),
    (r'^get-major-info/$', 'get_major_info', {}, 'get_major_info'),
    (r'^check-email-availability/$', 'check_email_availability', {}, 'check_email_availability'),
    (r'^check-email-existence/$', 'check_email_existence', {}, 'check_email_existence'),
    (r'^check-username-existence/$', 'check_username_existence', {}, 'check_username_existence'),
    (r'^check-campus-organization-uniqueness/$', 'check_campus_organization_uniqueness', {}, 'check_campus_organization_uniqueness'),
    (r'^check-language-uniqueness/$', 'check_language_uniqueness', {}, 'check_language_uniqueness'),
    (r'^check-event-name-uniqueness/$', 'check_event_name_uniqueness', {}, 'check_event_name_uniqueness'),
    (r'^check-website/$', 'check_website', {}, 'check_website')
)

urlpatterns += patterns('registration.views',
    (r'^login/', 'login', {}, 'login'),
    (r'^activation/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'activation_complete.html' }, 'activation_complete'),
    (r'^activation/(?P<activation_key>\w+)/$', 'activate_user', {}, 'student_activation'),
)

urlpatterns += patterns('student.views',
    # Student Registration
    (r'^student/registration/$', 'student_registration', {'extra_context': {'login_form':AuthenticationForm}}, "student_registration"),
    (r'^student/registration/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'student_registration_complete.html' }, 'student_registration_complete'),
    (r'^student/registration/closed/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'registration_closed.html' }, 'student_registration_closed'),
    # Student Profile Management
    (r'^student/edit-profile/$', 'student_edit_profile', {}, "student_edit_profile"),
    (r'^student/create-profile/$', 'student_create_profile', {}, "student_create_profile"),
    (r'^student/profile-form-tips-1/$', direct_to_template, {'template_name':'student_profile_form_tips_1.html'}, 'student_profile_form_tips_1'),
    (r'^student/create-campus-organization/$', 'student_create_campus_organization', {}, 'student_create_campus_organization'),
    (r'^student/create-language/$', 'student_create_language', {}, 'student_create_language'),
    (r'^student/update-resume/$', 'student_update_resume', {}, 'student_update_resume'),
    (r'^student/resume-info/$', 'student_resume_info', {}, 'resume_info'),
    # Student Account Settings
    (r'^student/account-settings/$', 'student_account_settings', {}, "student_account_settings"),   
    # Student Employer Subscriptions
    (r'^student/employer-subscriptions/$', 'student_employer_subscriptions', {}, 'student_employer_subscriptions'),
    # Student Invitations
    (r'^student/invitations/$', 'student_invitations', {}, 'student_invitations'),   
)

urlpatterns += patterns('employer.views',
    # Employer Registration
    (r'^employer/registration/$', 'employer_registration', {'extra_context': {'login_form':AuthenticationForm}}, 'employer_registration'),
    # Employer Account Settings
    (r'^employer/account-settings/$', 'employer_account_settings', {}, 'employer_account_settings'), 
    # Employer Student Filtering
    (r'^employer/add-to-resume-book/(?P<student_id>\d+)/$', 'employer_add_to_resume_book', {}, 'employer_add_to_resume_book'),
    (r'^employer/filtering-setup/$', 'employer_setup_default_filtering', {}, 'employer_setup_default_filtering'),
    (r'^employer/student-filtering/$', 'employer_student_filtering', {}, 'employer_student_filtering'),
    # Employer Events
    (r'^employer/events/new/$', 'employer_new_event', {}, 'employer_new_event'),
    (r'^employer/events/edit/(?P<id>\d+)$', 'employer_edit_event', {}, 'employer_edit_event'),
    (r'^employer/events/delete/(?P<id>\d+)$', 'employer_delete_event', {}, 'employer_delete_event'),
    # Employer Invitations
    (r'^employer/invitations/$', 'employer_invitations', {}, 'employer_invitations'),
    # Employer Company Profile
    (r'^employer/(?P<username>\w+)/$', 'employer_company_profile', {}, 'employer_company_profile'),
)

urlpatterns += patterns('events.views',
    (r'^events/$', 'events_list', {}, 'events_list'),
    (r'^events/(?P<id>\d+)/(?P<slug>[a-zA-Z-]+)$', 'event_page', {}, 'event_page'),
    (r'^events/rsvp/(?P<id>\d+)$', 'event_rsvp', {}, 'event_rsvp'),
    (r'^events/unrsvp/(?P<id>\d+)$', 'event_unrsvp', {}, 'event_unrsvp'),
)
