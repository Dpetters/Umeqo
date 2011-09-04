from core.model_helpers import generate_thumbnail
from subscription import signals

def create_thumbnail(sender, instance, created, raw, **kwargs):
    if instance.image and not instance.thumbnail:
        temp_name, content = generate_thumbnail(instance.image)
        instance.thumbnail.save(temp_name, content)

def delete_thumbnail_on_image_delete(sender, instance, created, raw, **kwargs):
    if not created and not raw and not instance.image and instance.thumbnail:
        instance.thumbnail.delete()

def impossible_downgrade(sender, subscription, **kwargs):
    before = sender.subscription
    after = subscription
    if not after.price:
        if before.price: return "You cannot downgrade to a free plan."
        else: return None
        
    if before.recurrence_unit:
        if not after.recurrence_unit:
            return "You cannot downgrade from recurring subscription to one-time."
        else:
            if after.price_per_day() > before.price_per_day(): return None
            else: return "You cannot downgrade to a cheaper plan."
    else:
        if not after.recurrence_unit:
            if after.price > before.price: return None
            else: return "You cannot downgrade to a cheaper plan."

__installed = False
def install():
    global __installed
    if not __installed:
        signals.change_check.connect(impossible_downgrade)
        __installed = True