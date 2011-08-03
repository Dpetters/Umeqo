from django.dispatch import receiver
from django.db.models import signals

from core.model_helpers import generate_thumbnail
from campus_org.models import CampusOrg
from core.models import Course

@receiver(signals.post_save, sender=CampusOrg)
@receiver(signals.post_save, sender=Course)
def create_recruiter_related_models(sender, instance, created, raw, **kwargs):
    if instance.image and not instance.thumbnail:
        temp_name, content = generate_thumbnail(instance.image)
        instance.thumbnail.save(temp_name, content)