from __future__ import division
from __future__ import absolute_import

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template, redirect_to

from core.forms import EmailAuthenticationForm as AuthenticationForm
from registration.forms import SetPasswordForm

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += patterns('',
    (r'^admin/django-ses/', include('django_ses.urls')),
)

if settings.USE_LANDING_PAGE:
    urlpatterns += patterns('',
        (r'^$', 'core.views.landing_page_wrapper', {'extra_context': {'login_form': AuthenticationForm}}),
    )
urlpatterns += patterns('',
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^notifications/', include('notification.urls')),
    # Hardcoded urls to eventually get rid of
    (r'^sbc-bbq/$', redirect_to, {'url':'/events/6/'}),
    (r'^events/36/alrightt/$', redirect_to, {'url':'/techfair/'}),
    (r'^techfair/$', redirect_to, {'url': '/techfair/fair/'}),
    (r'^employer/signup/$', redirect_to, {'url':'/subscriptions/'}),
    (r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'set_password_form':SetPasswordForm, 'template_name' : 'password_reset_new.html', 'extra_context': {'login_form':AuthenticationForm}}, 'password_reset_confirm'),
    (r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name' : 'password_successfully_changed.html', 'extra_context': {'login_form':AuthenticationForm}}, 'password_reset_complete'),
    (r'^password/reset/done/$', auth_views.password_reset_done, {'template_name' : 'password_reset_done.html', 'extra_context': {'login_form':AuthenticationForm}}, 'password_reset_done'),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^sentry/', include('sentry.web.urls')),
     url(r'zebra/',   include('zebra.urls',  namespace="zebra",  app_name='zebra') )
)
urlpatterns += patterns('newsletter.views',
    (r'^newsletter/(?P<year>\d+)/(?P<month>\w+)/$', 'newsletter', {}, 'newsletter'),
)
urlpatterns += patterns('core.views',
    (r'^$', 'home', {}, 'home'),
    (r'^favicon\.ico/$', redirect_to, {'url':'%simages/favicon.ico' % settings.STATIC_URL}),
    (r'^contact-us/$', 'contact_us', {}, 'contact_us'),
    (r'^terms/$', direct_to_template, {'template':'terms.html'}, 'terms'),
    (r'^terms/agree/$', 'terms_agree', {}, 'terms_agree'),
    (r'^help/$', 'help_center', {'extra_context': {'login_form': AuthenticationForm}}, 'help_center'),
    # Tutorials links to help center because I just put them there for now
    #(r'^help/tutorials/$', 'help_center', {'extra_context': {'login_form': AuthenticationForm}}, 'tutorials'),
    (r'^help/faq/$', 'faq', {'extra_context': {'login_form': AuthenticationForm}}, 'faq'),
    (r'^help/tutorials/(?P<slug>[0-9a-zA-Z-]+)/$', 'tutorial', {'extra_context': {'login_form': AuthenticationForm}}, 'tutorial'),
    (r'^about/$', 'about', {'extra_context': {'login_form': AuthenticationForm}}, 'about'),
    (r'^unsupported-browser/$', direct_to_template, { 'template' : 'browser_not_supported.html' }, 'unsupported_browser'),
    (r'^check-email-availability/$', 'check_email_availability', {}, 'check_email_availability'),
    (r'^check-employer-uniqueness/$', 'check_employer_uniqueness', {}, 'check_employer_uniqueness'),
    (r'^check-employer-campus-org-check-slug-uniqueness/$', 'check_employer_campus_org_slug_uniqueness', {}, 'check_employer_campus_org_slug_uniqueness'),    
    (r'^check-language-uniqueness/$', 'check_language_uniqueness', {}, 'check_language_uniqueness'),
    (r'^check-event-name-uniqueness/$', 'check_event_name_uniqueness', {}, 'check_event_name_uniqueness'),
    (r'^check-website/$', 'check_website', {}, 'check_website'),
    (r'^get-location-guess/$', 'get_location_guess', {}, 'get_location_guess'),
    (r'^get-location-suggestions/$', 'get_location_suggestions', {}, 'get_location_suggestions'),
    (r'^notification/count$', 'get_notice_unseen_count', {}, 'get_notice_unseen_count'),
    (r'^cache-status/$', 'cache_status', {}, 'cache_status'),
)
urlpatterns += patterns('campus_org.views',
    (r'^campus-org/registration/$', 'campus_org_registration', {'extra_context': {'password_min_length': settings.PASSWORD_MIN_LENGTH}}, "campus_org_registration"),
    (r'^campus-org/info/$', 'campus_org_info_dialog', {}, 'campus_org_info_dialog'),
    (r'^campus-org/check-uniqueness/$', 'check_campus_org_uniqueness', {}, 'check_campus_org_uniqueness'),
    (r'^campus-org/profile/$', 'campus_org_profile', {}, "campus_org_profile"),
    (r'^campus-org/account/$', 'campus_org_account', {'extra_context':{'password_min_length': settings.PASSWORD_MIN_LENGTH}}, 'campus_org_account'),
    (r'^campus-org/account/preferences/$', 'campus_org_account_preferences', {}, 'campus_org_account_preferences'),
    (r'^campus-org/registration/complete/$', 'campus_org_registration_complete', {}, 'campus_org_registration_complete'),
)
urlpatterns += patterns('registration.views',
    (r'^login/$', 'login', {'extra_context': {'authentication_form': AuthenticationForm}}, 'login'),
    (r'^super-login/$', 'super_login', {}, 'super_login'),
    (r'^logout/$', 'logout', {'login_url':'/?action=logged-out'}, 'logout'),
    (r'^password/change/$','password_change', {}, 'password_change'),
    (r'^resend_activation_email/$','resend_activation_email', {}, 'resend_activation_email'),
    (r'^password/reset/$', 'password_reset', {'extra_context': {'password_min_length': settings.PASSWORD_MIN_LENGTH, 'login_form':AuthenticationForm}}, 'password_reset'),
    (r'^activation/complete/$', direct_to_template, { 'extra_context': {'login_form':AuthenticationForm}, 'template': 'activation_complete.html' }, 'activation_complete'),
    (r'^activation/(?P<activation_key>\w+)/$', 'activate_user', {'extra_context': {'login_form': AuthenticationForm}}, 'student_activation'),

    )
urlpatterns += patterns('subscription.views',
    (r'^subscription/checkout/(?P<plan>\w+)/$', 'checkout', {}, 'checkout'),
    (r'^subscription/change/$', 'subscription_change', {}, 'subscription_change'),
    (r'^subscription/upgrade/(?P<subscription_type>\w+)/$', 'subscription_upgrade', {}, 'subscription_upgrade'),
    (r'^subscription/cancel/$', 'subscription_cancel', {}, 'subscription_cancel'),
    (r'^subscription/billing-cycle/change/$', 'subscription_billing_cycle_change', {}, 'subscription_billing_cycle_change'),
    (r'^account/request/$', 'account_request', {}, 'account_request'),
    (r'^payment/change/$', 'payment_change', {}, 'payment_change'),
    (r'^payment/cvc/help/$', direct_to_template, { 'template': 'payment_cvc_help_dialog.html' }, 'payment_cvc_help'),
    (r'^payment/forget/$', 'payment_forget', {}, 'payment_forget'),
    (r'^receipt/view/(?P<charge_id>\w+)/$', 'receipt_view', {}, 'receipt_view'),
    (r'^receipts/view/$', 'receipts_view', {}, 'receipts_view'),
    (r'^subscriptions/$', 'subscriptions', {'extra_context': {'login_form':AuthenticationForm}}, 'subscriptions'),
    (r'^webhooks/$', 'webhooks', {}, 'webhooks'),
    (r'^webhooks/v2/$', 'webhooks_v2', {}, 'webhooks_v2'),
)
urlpatterns += patterns('events.views',
    (r'^events/short-slug-uniqueness/$', 'events_check_short_slug_uniqueness', {}, 'events_check_short_slug_uniqueness'),
    (r'^events/(?P<id>\d+)/(?P<slug>[0-9a-zA-Z-]+)/$', 'event_page', {'extra_context': {'login_form':AuthenticationForm}}, 'event_page'),
    (r'^events/(?P<id>\d+)/$', 'event_page_redirect', {}, 'event_page_redirect'),
    (r'^events/export/$', 'event_list_export', {}, 'event_list_export'),
    (r'^events/admin/campusorg/upload-recruiter-list/$', 'event_upload_recruiters_list', {}, 'event_upload_recruiters_list'),
    (r'^events/export/download/$', 'event_list_download', {}, 'event_list_download'),
    (r'^events/export/completed/$', 'event_list_export_completed', {}, 'event_list_export_completed'),
    (r'^events/checkin/(?P<event_id>\d+)$', 'event_checkin', {}, 'event_checkin'),
    (r'^events/checkin/count/$', 'event_checkin_count', {}, 'event_checkin_count'),
    (r'^events/raffle-winner/$', 'event_raffle_winner', {}, 'event_raffle_winner'),
    (r'^events/rsvp/(?P<event_id>\d+)$', 'event_rsvp', {}, 'event_rsvp'),
    (r'^events/rsvp/message/$', 'event_rsvp_message', {}, 'event_rsvp_message'),
    (r'^events/drop/(?P<event_id>\d+)$', 'event_drop', {}, 'event_drop'),
    (r'^events/e/$', 'events_by_employer', {}, 'events_by_employer'),
    (r'^events/i/$', 'event_invite', {}, 'event_invite'),
    (r'^events/archive/(?P<id>\d+)$', 'event_archive', {}, 'event_archive'),
    (r'^events/new/$', 'event_new', {}, 'event_new'),
    (r'^events/cancel/(?P<id>\d+)$', 'event_cancel', {}, 'event_cancel'),
    (r'^events/edit/(?P<id>\d+)$', 'event_edit', {}, 'event_edit'),
    (r'^events/schedule/$', 'event_schedule', {}, 'event_schedule'),
    (r'^rolling-deadline/end/(?P<id>\d+)$', 'rolling_deadline_end', {}, 'rolling_deadline_end'),
    (r'^events/$', redirect_to, {'url':'/events/upcoming/'}, 'upcoming_events'),
    (r'^events/(?P<category>\w+)/$', 'events', {}, 'events'),
    (r'^event/(?P<event_id>\d+)/download-participant-resumes/$', 'download_event_participant_resumes', {}, 'download_event_participant_resumes')
)
urlpatterns += patterns('student.views',
    (r'^signup/$', 'student_registration', {'extra_context': {'password_min_length': settings.PASSWORD_MIN_LENGTH, 'login_form':AuthenticationForm}}, "student_registration"),
    (r'^signup/quick/$', 'student_quick_registration', {}, 'student_quick_registration'),
    (r'^signup/quick/done/$', 'student_quick_registration_done', {}, 'student_quick_registration_done'),
    (r'^student/registration/complete/$', 'student_registration_complete', { 'extra_context': {'login_form':AuthenticationForm}}, 'student_registration_complete'),
    (r'^student/registration/closed/$', direct_to_template, {'template' : 'student_registration_closed.html', 'extra_context': {'login_form':AuthenticationForm}}, "student_registration_closed"),
    (r'^student/profile/unparsable-resume/$', 'student_profile_unparsable_resume', {}, "student_profile_unparsable_resume"),
    (r'^student/profile/preview/$', 'student_profile_preview', {}, "student_profile_preview"),
    (r'^student/profile/$', 'student_profile', {}, "student_profile"),
    (r'^student/create-campus-org/$', 'student_create_campus_org', {}, 'student_create_campus_org'),
    (r'^student/create-language/$', 'student_create_language', {}, 'student_create_language'),
    (r'^student/update-resume/$', 'student_update_resume', {}, 'student_update_resume'),
    (r'^student/update-resume/info/$', 'student_update_resume_info', {}, 'student_update_resume_info'),
    (r'^student/account/$', 'student_account', {'extra_context':{'password_min_length': settings.PASSWORD_MIN_LENGTH}}, "student_account"),
    (r'^student/account/preferences/$', 'student_account_preferences', {}, "student_account_preferences"),
    (r'^student/account/deactivate/$', 'student_account_deactivate', {}, "student_account_deactivate"),
    (r'^student/resume/$', 'student_resume', {}, 'student_resume'),
    (r'^student/resume/(?P<student_id>\d+)/$', 'specific_student_resume', {}, 'specific_student_resume'),
    (r'^student/resume/increment-view-count/$', 'student_increment_resume_view_count', {}, 'student_increment_resume_view_count')
)
urlpatterns += patterns('employer.views',
    (r'^employer/logo/$', 'employer_logo', {}, 'employer_logo'),
    (r'^employer/new/$', 'employer_new', {}, 'employer_new'),
    (r'^employer/details/$', 'employer_details', {}, 'employer_details'),
    (r'^employer/subscribe/$', 'employer_subscribe', {}, 'employer_subscribe'),
    (r'^employer/account/$', 'employer_account', {'extra_context':{'password_min_length': settings.PASSWORD_MIN_LENGTH}}, 'employer_account'),
    (r'^employer/account/delete/$', 'employer_account_delete', {}, 'employer_account_delete'),
    (r'^employer/account/preferences/$', 'employer_account_preferences', {}, 'employer_account_preferences'),
    (r'^employer/profile/$', 'employer_profile', {}, "employer_profile"),
    (r'^employer/recruiters/other/$', 'employer_other_recruiters', {}, 'employer_other_recruiters'),
    (r'^employer/recruiters/new/$', 'employer_recruiter_new', {}, 'employer_recruiter_new'),
    (r'^employer/students/$', 'employer_students', {}, 'employer_students'),
    (r'^employer/students/toggle-star/$', 'employer_student_toggle_star', {}, 'employer_student_toggle_star'),
    (r'^employer/students/add-star/$', 'employer_students_add_star', {}, 'employer_students_add_star'),
    (r'^employer/students/remove-star/$', 'employer_students_remove_star', {}, 'employer_students_remove_star'),
    (r'^employer/students/comment/$', 'employer_student_comment', {}, 'employer_student_comment'),
    (r'^employer/students/event-attendance/$', 'employer_student_event_attendance', {}, 'employer_student_event_attendance'),  
    (r'^employer/resume-books/history/$', 'employer_resume_book_history', {}, 'employer_resume_book_history'),
    (r'^employer/resume-books/current/delivered/$', direct_to_template, {'template':'employer_resume_book_delivered.html'}, 'employer_resume_book_delivered'),
    (r'^employer/resume-books/current/deliver/download/$', 'employer_resume_book_download', {}, 'employer_resume_book_download'),
    (r'^employer/resume-books/current/deliver/email/$', 'employer_resume_book_email', {}, 'employer_resume_book_email'),
    (r'^employer/resume-books/current/deliver/$', 'employer_resume_book_deliver', {}, 'employer_resume_book_deliver'),
    (r'^employer/resume-books/current/create/$', 'employer_resume_book_create', {}, 'employer_resume_book_create'),
    (r'^employer/resume-books/current/summary/$', 'employer_resume_book_summary', {}, 'employer_resume_book_summary'),
    (r'^employer/resume-books/current/toggle-student/$', 'employer_resume_book_toggle_student', {}, 'employer_resume_book_toggle_student'),
    (r'^employer/resume-books/current/add-students/$', 'employer_resume_book_add_students', {}, 'employer_resume_book_add_students'),
    (r'^employer/resume-books/current/remove-students/$', 'employer_resume_book_remove_students', {}, 'employer_resume_book_remove_students'),
    (r'^employer/resume-books/delete/$', 'employer_resume_book_delete', {}, 'employer_resume_book_delete'),
    (r'^employer/resumes/download/$', 'employer_resumes_download', {}, 'employer_resumes_download'),
    (r'^employers/snippets/$', 'employer_snippets', {}, 'employer_snippets'),
    (r'^employers/$', 'employers', {}, 'employers'),
    (r'^(?P<slug>[A-Za-z0-9-]+)/$', 'employer_profile_preview', {}, 'employer_profile_preview')
)

urlpatterns += patterns('events.views',
    (r'^(?P<owner_slug>\w+)/(?P<event_slug>\w+)/$', 'events_shortcut', {}, 'events_shortcut')
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    
handler500 = 'core.views.handle_500'
handler404 = 'core.views.handle_404'
handler403 = 'core.views.handle_403'
