from django.db import models

from core.model_helpers import get_campus_org_image_filename, get_campus_org_thumbnail_filename
from core.models import CommonInfo, CampusOrgType


class CampusOrg(CommonInfo):
    name = models.CharField("On-Campus Organization Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    type = models.ForeignKey(CampusOrgType)
    image = models.ImageField(upload_to=get_campus_org_image_filename, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_campus_org_thumbnail_filename, blank=True, null=True)

    class Meta(CommonInfo.Meta):
        verbose_name = "On-Campus Organization"
        verbose_name_plural = "On-Campus Organizations"
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
