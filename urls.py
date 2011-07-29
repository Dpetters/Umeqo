from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

from core.forms import EmailAuthenticationForm as AuthenticationForm
from registration.forms import PasswordResetForm, SetPasswordForm

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
if settings.USE_LANDING_PAGE:
    urlpatterns += patterns('',
        (r'^$', 'core.views.landing_page', {'extra_context': {'login_form': AuthenticationForm}}),
    )
urlpatterns += patterns('',
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
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
    (r'^unsupported-browser/$', 'unsupported_browser', {}, 'unsupported_browser'),
    (r'^course-info/$', 'course_info', {}, 'course_info'),
    (r'^get-campus-org-info/$', 'campus_org_info', {}, 'campus_org_info'),
    (r'^check-email-availability/$', 'check_email_availability', {}, 'check_email_availability'),
    (r'^check-email-existence/$', 'check_email_existence', {}, 'check_email_existence'),
    (r'^check-username-existence/$', 'check_username_existence', {}, 'check_username_existence'),
    (r'^check-campus-organization-uniqueness/$', 'check_campus_organization_uniqueness', {}, 'check_campus_organization_uniqueness'),
    (r'^check-language-uniqueness/$', 'check_language_uniqueness', {}, 'check_language_uniqueness'),
    (r'^check-event-name-uniqueness/$', 'check_event_name_uniqueness', {}, 'check_event_name_uniqueness'),
    (r'^check-website/$', 'check_website', {}, 'check_website'),
    (r'^get-location-suggestions/$', 'get_location_suggestions', {}, 'get_location_suggestions'),
    (r'^notification/count$', 'get_notice_unseen_count', {}, 'get_notice_unseen_count'),
)

urlpatterns += patterns('registration.views',
    (r'^login/$', 'login', {'extra_context': {'authentication_form': AuthenticationForm}}, 'login'),
    (r'^logout/$', 'logout', {'login_url':'/?action=logged-out'}, 'logout'),
    (r'^password/change/$','password_change', {}, 'password_change'),
    (r'^activation/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'activation_complete.html' }, 'activation_complete'),
    (r'^activation/(?P<activation_key>\w+)/$', 'activate_user', {}, 'student_activation'),
)
urlpatterns += patterns('student.views',
    (r'^signup/$', 'student_registration', {'extra_context': {'login_form':AuthenticationForm}}, "student_registration"),
    (r'^student/registration/complete/$', 'student_registration_complete', { 'extra_context': {'login_form':AuthenticationForm}}, 'student_registration_complete'),
    (r'^student/profile/unparsable-resume/$', direct_to_template, {'template' : 'student_profile_unparsable_resume.html'}, "student_profile_unparsable_resume"),
    (r'^student/profile/preview/$', 'student_profile_preview', {}, "student_profile_preview"),
    (r'^student/profile/$', 'student_profile', {}, "student_profile"),
    (r'^student/profile-form-tips-1/$', direct_to_template, {'template':'student_profile_form_tips_1.html'}, 'student_profile_form_tips_1'),
    (r'^student/create-campus-organization/$', 'student_create_campus_organization', {}, 'student_create_campus_organization'),
    (r'^student/create-language/$', 'student_create_language', {}, 'student_create_language'),
    (r'^student/update-resume/$', 'student_update_resume', {}, 'student_update_resume'),
    (r'^student/update-resume/info/$', 'student_update_resume_info', {}, 'student_update_resume_info'),
    (r'^student/account/$', 'student_account_settings', {}, "student_account_settings"),
    (r'^student/account/deactivate/$', 'student_account_deactivate', {}, "student_account_deactivate"),
    (r'^student/employer-subscriptions/$', 'student_employer_subscriptions', {}, 'student_employer_subscriptions'),
    (r'^student/invitations/$', 'student_invitations', {}, 'student_invitations'),
    (r'^student/resume/$', 'student_resume', {}, 'student_resume'),
)
urlpatterns += patterns('employer.views',
    (r'^employer/registration/$', 'employer_registration', {'extra_context': {'login_form':AuthenticationForm}}, 'employer_registration'),
    (r'^employer/account-settings/$', 'employer_account_settings', {}, 'employer_account_settings'),
    (r'^employer/students/*$', 'employer_students', {}, 'employer_students'),
    (r'^employer/students/default-filtering/$', 'employer_students_default_filtering', {}, 'employer_students_default_filtering'),
    (r'^employer/students/toggle-star/$', 'employer_student_toggle_star', {}, 'employer_student_toggle_star'),    
    (r'^employer/students/add-star/$', 'employer_students_add_star', {}, 'employer_students_add_star'),   
    (r'^employer/students/remove-star/$', 'employer_students_remove_star', {}, 'employer_students_remove_star'),    
    (r'^employer/students/comment/$', 'employer_student_comment', {}, 'employer_student_comment'),
    (r'^employer/students/event-attendance/$', 'employer_student_event_attendance', {}, 'employer_student_event_attendance'),  
    (r'^employer/resume-books/$', 'employer_resume_books', {}, 'employer_resume_books'),
    (r'^employer/resume-books/current/delivered/$', direct_to_template, {'template':'employer_resume_book_current_delivered.html'}, 'employer_resume_book_current_delivered'),
    (r'^employer/resume-books/current/deliver/download/$', 'employer_resume_book_current_download', {}, 'employer_resume_book_current_download'),
    (r'^employer/resume-books/current/deliver/email/$', 'employer_resume_book_current_email', {}, 'employer_resume_book_current_email'),    
    (r'^employer/resume-books/current/deliver/$', 'employer_resume_book_current_deliver', {}, 'employer_resume_book_current_deliver'),
    (r'^employer/resume-books/current/create/$', 'employer_resume_book_current_create', {}, 'employer_resume_book_current_create'),
    (r'^employer/resume-books/current/summary/$', 'employer_resume_book_current_summary', {}, 'employer_resume_book_current_summary'),    
    (r'^employer/resume-books/current/toggle-student/$', 'employer_resume_book_current_toggle_student', {}, 'employer_resume_book_current_toggle_student'),
    (r'^employer/resume-books/current/add-students/$', 'employer_resume_book_current_add_students', {}, 'employer_resume_book_current_add_students'),
    (r'^employer/resume-books/current/remove-students/$', 'employer_resume_book_current_remove_students', {}, 'employer_resume_book_current_remove_students'),  
    (r'^employer/events/new/$', 'employer_event_new', {}, 'employer_event_new'),
    (r'^employer/events/edit/(?P<id>\d+)$', 'employer_event_edit', {}, 'employer_event_edit'),
    (r'^employer/events/delete/(?P<id>\d+)$', 'employer_event_delete', {}, 'employer_event_delete'),
    (r'^employer/invitations/$', 'employer_invitations', {}, 'employer_invitations'),
    (r'^employer/(?P<employer>\w+)/$', 'employer_profile', {}, 'employer_profile'),
    (r'^employers/pane/$', 'employers_list_pane', {}, 'employers_list_pane'),
    (r'^employers/$', 'employers_list', {}, 'employers_list'),
    (r'^employers/ajax$', 'employer_list_ajax', {}, 'employers_list_ajax'),
    (r'^employers/subscribe$', 'employer_subscribe', {}, 'employers_subscribe')
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
    (r'^events/e/$', 'events_by_employer', {}, 'events_by_employer'),
    (r'^events/i/$', 'event_invite', {}, 'event_invite'),
)
urlpatterns += staticfiles_urlpatterns()