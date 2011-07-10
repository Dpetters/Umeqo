from django.conf import settings
from django.db.models import signals

if 'notification' in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type('new_event', 'New Event', 'an employer has created a new event')
        notification.create_notice_type('public_invite', 'Public Event invite', 'an employer has invited you to an event')

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Not creating notice types - notification app not found"
