from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from core.model_helpers import get_image_filename, get_thumbnail_filename
from core.models import CommonInfo
from core.signals import create_thumbnail, delete_thumbnail_on_image_delete
from core import mixins as core_mixins

class CampusOrg(CommonInfo):
    user = models.OneToOneField(User, unique=True, null=True, blank=True)
    name = models.CharField("On-Campus Organization Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    type = models.ForeignKey("core.CampusOrgType")
    image = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_thumbnail_filename, blank=True, null=True)

    class Meta(CommonInfo.Meta):
        verbose_name = "On-Campus Organization"
        verbose_name_plural = "On-Campus Organizations"
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

post_save.connect(create_thumbnail, sender=CampusOrg)
post_save.connect(delete_thumbnail_on_image_delete, sender=CampusOrg)


class CampusOrgPreferences(core_mixins.DateTracking):
    campus_org = models.OneToOneField("campus_org.CampusOrg", unique=True, editable=False)
    

    class Meta:
        verbose_name = "Campus Org Preferences"
        verbose_name_plural = "Camput Org Preferences"
    
    def __unicode__(self):
        if hasattr(self, "campus_org"):
            return "Campus Org Preferences for %s" % (self.campus_org,)
        else:
            return "Unattached Campus Org Preferences"


class CampusOrgStatistics(core_mixins.DateTracking):
    campus_org = models.OneToOneField("campus_org.CampusOrg", unique=True, editable=False)

    class Meta:
        verbose_name = "Campus Org Statistics"
        verbose_name_plural = "Campus Org Statistics"

    def __unicode__(self):
        if hasattr(self, "campus_org"):
            return "Campus Org Statistics for %s" % (self.student,)
        else:
            return "Unattached Campus Org Statistics"
