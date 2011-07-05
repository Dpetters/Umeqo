"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

from registration.forms import PasswordResetForm, SetPasswordForm

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.USE_LANDING_PAGE:
    urlpatterns += patterns('',
        (r'^$', 'core.views.landing_page'),
    )

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^messages/', include('messages.urls')),
    (r'^notifications/', include('notification.urls')),
    (r'^password/reset/$', auth_views.password_reset, {'password_reset_form':PasswordResetForm, 'template_name' : 'password_reset_form.html', 'email_template_name': 'password_reset_email.html', 'extra_context': {'login_form':AuthenticationForm}}, 'auth_password_reset'),
    (r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'set_password_form':SetPasswordForm, 'template_name' : 'password_reset_confirm.html', 'extra_context': {'login_form':AuthenticationForm}}, 'auth_password_reset_confirm'),
    (r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name' : 'password_successfully_changed.html', 'extra_context': {'login_form':AuthenticationForm}}, 'auth_password_reset_complete'),
    (r'^password/reset/done/$', auth_views.password_reset_done, {'template_name' : 'password_reset_done.html', 'extra_context': {'login_form':AuthenticationForm}}, 'auth_password_reset_done'),
)

urlpatterns += patterns('core.views',
    (r'^$', 'home', {}, 'home'),
    (r'^contact-us-dialog/$', 'contact_us_dialog', {}, 'contact_us_dialog'),
    (r'^help/$', 'help_center', {'extra_context': {'login_form': AuthenticationForm}}, 'help_center'),
    (r'^help/faq/$', 'faq', {'extra_context': {'login_form': AuthenticationForm}}, 'faq'),
    (r'^help/tutorials/$', 'tutorials', {'extra_context': {'login_form': AuthenticationForm}}, 'tutorials'),
    (r'^about/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'about.html' }, 'about'),
    (r'^blog/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template' : 'blog.html' }, 'blog'),
    (r'^browser-configuration-not-supported/$', 'browser_configuration_not_supported', {}, 'browser_configuration_not_supported'),
    (r'^get-course-info/$', 'get_course_info', {}, 'get_course_info'),
    (r'^get-campus-org-info/', 'get_campus_org_info', {}, 'get_campus_org_info'),
    (r'^check-email-availability/$', 'check_email_availability', {}, 'check_email_availability'),
    (r'^check-email-existence/$', 'check_email_existence', {}, 'check_email_existence'),
    (r'^check-username-existence/$', 'check_username_existence', {}, 'check_username_existence'),
    (r'^check-campus-organization-uniqueness/$', 'check_campus_organization_uniqueness', {}, 'check_campus_organization_uniqueness'),
    (r'^check-language-uniqueness/$', 'check_language_uniqueness', {}, 'check_language_uniqueness'),
    (r'^check-event-name-uniqueness/$', 'check_event_name_uniqueness', {}, 'check_event_name_uniqueness'),
    (r'^check-website/$', 'check_website', {}, 'check_website'),
)

urlpatterns += patterns('registration.views',
    (r'^login/', 'login', {}, 'login'),
    (r'^logout/$', 'logout', {'login_url':'/?action=logged-out'}, 'logout'),
    (r'^password/change/$','password_change', {}, 'password_change'),
    (r'^activation/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'activation_complete.html' }, 'activation_complete'),
    (r'^activation/(?P<activation_key>\w+)/$', 'activate_user', {}, 'student_activation'),
)

urlpatterns += patterns('student.views',
    # Student Registration
    (r'^student/registration/$', 'student_registration', {'extra_context': {'login_form':AuthenticationForm}}, "student_registration"),
    (r'^student/registration/complete/$', 'student_registration_complete', { 'extra_context': {'login_form':AuthenticationForm}}, 'student_registration_complete'),
    # Student Profile Management
    (r'^student/edit-profile/$', 'student_edit_profile', {}, "student_edit_profile"),
    (r'^student/create-profile/$', 'student_create_profile', {}, "student_create_profile"),
    (r'^student/profile-form-tips-1/$', direct_to_template, {'template_name':'student_profile_form_tips_1.html'}, 'student_profile_form_tips_1'),
    (r'^student/create-campus-organization/$', 'student_create_campus_organization', {}, 'student_create_campus_organization'),
    (r'^student/create-language/$', 'student_create_language', {}, 'student_create_language'),
    (r'^student/update-resume/$', 'student_update_resume', {}, 'student_update_resume'),
    (r'^student/update-resume/info/$', 'student_update_resume_info', {}, 'student_update_resume_info'),
    # Student Account Settings
    (r'^student/account-settings/$', 'student_account_settings', {}, "student_account_settings"),
    # Student Employer Subscriptions
    (r'^student/employer-subscriptions/$', 'student_employer_subscriptions', {}, 'student_employer_subscriptions'),
    # Student Invitations
    (r'^student/invitations/$', 'student_invitations', {}, 'student_invitations'),
    # Student Resume
    (r'^student/resume/$', 'student_resume', {}, 'student_resume'),
)

urlpatterns += patterns('employer.views',
    # Employer List
    (r'^employers/pane/$', 'employers_list_pane', {}, 'employers_list_pane'),
    (r'^employers/$', 'employers_list', {}, 'employers_list'),
    (r'^employers/ajax$', 'employers_list_ajax', {}, 'employers_list_ajax'),
    (r'^employers/subscribe$', 'employers_subscribe', {}, 'employers_subscribe'),
    # Employer Registration
    (r'^employer/registration/$', 'employer_registration', {'extra_context': {'login_form':AuthenticationForm}}, 'employer_registration'),
    # Employer Account Settings
    (r'^employer/account-settings/$', 'employer_account_settings', {}, 'employer_account_settings'),
    # Employer Student Filtering
    (r'^employer/filtering-setup/$', 'employer_setup_default_filtering', {}, 'employer_setup_default_filtering'),
    (r'^employer/resume-books/download/$', 'employer_resume_books_download', {}, 'employer_resume_books_download'),
    (r'^employer/resume-books/email/$', 'employer_resume_books_email', {}, 'employer_resume_books_email'),    
    (r'^employer/resume-books/deliver/$', 'employer_resume_books_deliver', {}, 'employer_resume_books_deliver'),
    (r'^employer/resume-books/create/$', 'employer_resume_books_create', {}, 'employer_resume_books_create'),
    (r'^employer/resume-book/summary/$', 'employer_resume_book_summary', {}, 'employer_resume_book_summary'),    
    (r'^employer/resume-book/student/toggle/$', 'employer_resume_book_student_toggle', {}, 'employer_resume_book_student_toggle'),
    (r'^employer/resume-book/students/add/$', 'employer_resume_book_students_add', {}, 'employer_resume_book_students_add'),
    (r'^employer/resume-book/students/remove/$', 'employer_resume_book_students_remove', {}, 'employer_resume_book_students_remove'),
    (r'^employer/star/student/toggle/$', 'employer_star_student_toggle', {}, 'employer_star_student_toggle'),    
    (r'^employer/star/students/add/$', 'employer_star_students_add', {}, 'employer_star_students_add'),   
    (r'^employer/star/students/remove/$', 'employer_star_students_remove', {}, 'employer_star_students_remove'),    
    (r'^employer/students/*$', 'employer_students', {}, 'employer_students'),
    (r'^employer/students/comment/$', 'employer_students_comment', {}, 'employer_students_comment'),
    # Employer Events
    (r'^employer/events/new/$', 'employer_new_event', {}, 'employer_new_event'),
    (r'^employer/events/edit/(?P<id>\d+)$', 'employer_edit_event', {}, 'employer_edit_event'),
    (r'^employer/events/delete/(?P<id>\d+)$', 'employer_delete_event', {}, 'employer_delete_event'),
    # Employer Invitations
    (r'^employer/invitations/$', 'employer_invitations', {}, 'employer_invitations'),
    # Employer Profile
    (r'^employer/(?P<employer>\w+)/$', 'employer_employer_profile', {}, 'employer_employer_profile'),
)

urlpatterns += patterns('events.views',
    (r'^events/$', 'events_list', {}, 'events_list'),
    (r'^events/(?P<id>\d+)/(?P<slug>[0-9a-zA-Z-]+)$', 'event_page', {'extra_context': {'login_form':AuthenticationForm}}, 'event_page'),
    (r'^events/(?P<id>\d+)/?$', 'event_page_redirect', {}, 'event_page_redirect'),
    (r'^events/checkin/(?P<id>\d+)$', 'event_checkin', {}, 'event_checkin'),
    (r'^events/rsvp/(?P<id>\d+)$', 'event_rsvp', {}, 'event_rsvp'),
    (r'^events/unrsvp/(?P<id>\d+)$', 'event_unrsvp', {}, 'event_unrsvp'),
    (r'^events/checkin/(?P<id>\d+)$', 'event_checkin', {}, 'event_checkin'),
    (r'^events/search/$', 'event_search', {}, 'event_search'),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('notification.views',
    (r'^notification/ajax$', 'notices', {}, 'notification_ajax'),
)
