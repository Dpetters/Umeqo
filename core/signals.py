from core.model_helpers import generate_thumbnail
from notification import models as notification
from django.db.models.signals import post_syncdb

def create_thumbnail(sender, instance, created, raw, **kwargs):
    if instance.image and not instance.thumbnail:
        temp_name, content = generate_thumbnail(instance.image)
        instance.thumbnail.save(temp_name, content)

def delete_thumbnail_on_image_delete(sender, instance, created, raw, **kwargs):
    if not created and not raw and not instance.image and instance.thumbnail:
        instance.thumbnail.delete()

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type('new_event', 'New Event', 'an employer has created a new event')
    notification.create_notice_type('public_invite', 'Public Event Invite', 'an employer has invited you to an event')
    notification.create_notice_type('private_invite', 'Private Event Invite', 'an employer has invited you to an event')
post_syncdb.connect(create_notice_types, sender=notification)