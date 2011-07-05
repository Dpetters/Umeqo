from django.conf import settings
from django.db.models import signals

if 'notification' in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        print "Creating notification types..."
        notification.create_notice_type('new_event', 'New Event', 'an employer has created a new event')

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Not creating notice types - notification app not found"
