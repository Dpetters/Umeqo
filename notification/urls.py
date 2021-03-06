from django.conf.urls.defaults import patterns

from notification.views import notices, single, notification_ajax

urlpatterns = patterns('',
    (r'^$', notices, {}, "notification_notices"),
    #(r'^settings/$', notice_settings, {}, "notification_notice_settings"),
    (r'^(\d+)/$', single, {}, "notification_notice"),
    #(r'^feed/$', feed_for_user, {}, "notification_feed_for_user"),
    #(r'^mark_all_seen/$', mark_all_seen, {}, "notification_mark_all_seen"),
    (r'^notification/ajax/$', notification_ajax, {}, "notification_ajax"),
)
