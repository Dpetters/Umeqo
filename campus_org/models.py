from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from core.model_helpers import get_image_filename, get_thumbnail_filename
from core.models import CommonInfo
from core.signals import create_thumbnail, delete_thumbnail_on_image_delete
from core import mixins as core_mixins


class CampusOrg(CommonInfo):
    user = models.ForeignKey(User, null=True, blank=True)
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
    student = models.OneToOneField("student.Student", unique=True, editable=False)
    
    email_on_invite_to_public_event = models.BooleanField(default=True)
    email_on_invite_to_private_event = models.BooleanField(default=True)
    email_on_new_subscribed_employer_event = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Student Preferences"
        verbose_name_plural = "Student Preferences"
    
    def __unicode__(self):
        if hasattr(self, "student"):
            return "Student Preferences for %s" % (self.student,)
        else:
            return "Unattached Student Preferences"


class CampusOrgStatistics(core_mixins.DateTracking):
    student = models.OneToOneField("student.Student", unique=True, editable=False)
    
    event_invite_count = models.PositiveIntegerField(editable=False, default = 0)
    add_to_resumebook_count = models.PositiveIntegerField(editable=False, default = 0)
    resume_view_count = models.PositiveIntegerField(editable=False, default = 0)
    shown_in_results_count = models.PositiveIntegerField(editable=False, default = 0)

    class Meta:
        verbose_name = "Student Statistics"
        verbose_name_plural = "Student Statistics"

    def __unicode__(self):
        if hasattr(self, "student"):
            return "Student Statistics for %s" % (self.student,)
        else:
            return "Unattached Student Statistics"