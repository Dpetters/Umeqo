"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.conf.urls.defaults import patterns, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()
import haystack
haystack.autodiscover()
from student.forms import create_profile_form, edit_profile_form

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^notifications/', include('notification.urls')),
)
urlpatterns += patterns('registration.views',
    (r'^$', 'home', {}, 'home'),
    (r'^login_dialog', 'login_dialog', {}, 'login_dialog'),
    (r'^login_redirect', 'login_redirect', {}, 'login_redirect'),
    (r'^logout/$', auth_views.logout),
    (r'^password/change/$', 'password_change', {}, 'password_change'),
    (r'^password/change/done/$', 'password_change_done', {}, 'password_change_done'),
)
urlpatterns += patterns('student.views',
    (r'^student/get-suggested-employers-list/$', 'student_get_suggested_employers_list'),
    (r'^student/profile-form-info/$', 'student_profile_form_info'),
    (r'^student/create-campus-organization/$', 'student_create_campus_organization'),
    (r'^student/create-language/$', 'student_create_language'),
    (r'^student/employer-subscriptions-dialog/$', 'student_employer_subscriptions'),
    (r'^student/events/$', 'student_events', {}, 'student_events'),
    (r'^student/events/(?P<employer>\w+)/$', 'student_events', {}, 'student_events'),
    (r'^student/edit', 'edit_profile', {'form_class': edit_profile_form }, "student_edit_profile"),
    (r'^student/create', 'create_profile', {'form_class': create_profile_form }, "student_create_profile"),
    (r'^student/', include('registration.backends.default.urls')),
    (r'^student/(?P<username>\w+)/$', 'student_home', {}, "student_home"),
    (r'^resume_update', 'resume_update'),
)
urlpatterns += patterns('core.views',
    (r'^enable-javascript/$', 'enable_javascript', {}, 'enable_javascript'),
    (r'^browser-not-supported/$', 'browser_not_supported', {}, 'browser_not_supported'),
    (r'^about/$', 'about', {}, 'about'),
    (r'^faq/$', 'faq', {}, 'faq'),
    (r'^blog/$', 'blog', {}, 'blog'),
    (r'^advertise/$', 'advertise', {}, 'advertise'),
)

urlpatterns += patterns('employer.views',
    (r'^employer/add-to-resume-book/(?P<student_id>\d+)/$', 'employer_add_to_resume_book', {}, 'employer_add_to_resume_book'),
    (r'^employer/filtering/$', 'employer_filtering', {}, 'employer_filtering'),
    (r'^employer/results/$', 'employer_filtering_results', {}, 'employer_filtering_results'),
    (r'^employer/setup-default-filtering-parameters', 'employer_setup_default_filtering_parameters', {}, 'employer_setup_default_filtering_parameters'),
    (r'^employer/register/$', 'employer_register', {}, 'employer_register'),
    (r'^employer/events/$', 'employer_events', {}, 'employer_events'),
    (r'^employer/events/(?P<id>\d+)/$', 'employer_event', {}, 'employer_event'),
    (r'^employer/events/new/$', 'employer_new_event', {}, 'employer_new_event'),
    (r'^employer/(?P<username>\w+)/$', 'employer_home', {}, 'employer_home'),
)
urlpatterns += patterns('contact_form.views',
    (r'^contact_us_dialog/$', 'contact_us_dialog', {}, 'contact_us_dialog'),
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