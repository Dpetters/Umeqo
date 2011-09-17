from django.dispatch import Signal

from core.model_helpers import generate_thumbnail

us_user_logged_in = Signal(providing_args=['request', 'user', 'super'])

def create_thumbnail(sender, instance, created, raw, **kwargs):
    if instance.image and not instance.thumbnail:
        temp_name, content = generate_thumbnail(instance.image)
        instance.thumbnail.save(temp_name, content)

def delete_thumbnail_on_image_delete(sender, instance, created, raw, **kwargs):
    if not created and not raw and not instance.image and instance.thumbnail:
        instance.thumbnail.delete()
