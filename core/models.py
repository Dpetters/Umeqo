from django.db import models
from django.db.models import signals
from notification import models as notification
from django.dispatch import receiver

from core.model_helpers import get_course_image_filename, get_campus_org_image_filename, get_course_thumbnail_filename, get_campus_org_thumbnail_filename, generate_thumbnail
from core import enums
from core import mixins as core_mixins


class Location(models.Model):
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    keywords = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, verify_exists=False)
    building_num = models.CharField(max_length = 10, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        if self.display_name:
            return self.display_name
        elif self.building_num:
            return "%s (Building %s)" % (self.name, self.building_num)
        else:
            return self.name     


class Topic(core_mixins.DateTracking):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    sort_order = models.DecimalField(decimal_places=3, max_digits=6, help_text='Topics will be ordered by the sort order. (Smallest at top.)')

    class Meta:
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.name


class Question(core_mixins.DateTracking):
    topic = models.ForeignKey(Topic)
    display = models.BooleanField(help_text="Only select if all of the above info has been checked for errors and finalized.")
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES, default=enums.ALL)
    sort_order = models.DecimalField(decimal_places=3, max_digits=6, help_text='Topics will be ordered by the sort order. (Smallest at top.)')
    question = models.TextField()
    answer = models.TextField() 
    slug = models.SlugField( max_length=100, help_text="This is a unique identifier that allows your questions to display its detail view, ex 'how-can-i-contribute'", )

    class Meta:
        ordering = ['sort_order', 'question']
        
    def __unicode__(self):
        return self.question
        
         
class CommonInfo(core_mixins.DateTracking):
    email = models.EmailField("Contact E-mail", blank=True, null=True)
    website = models.URLField(blank=True, null=True, verify_exists=False)
    description = models.TextField(max_length=500, blank=True, null=True, help_text="Maximum 500 characters.")
    display = models.BooleanField(help_text="Only select if all of the above info has been checked for errors and finalized.")

    class Meta:
        abstract = True
 
 
class SchoolYear(core_mixins.DateTracking):
    name = models.CharField("School Year", max_length=42, unique=True, help_text="Maximum 42 characters.")

    class Meta:
        verbose_name = "School Year"
        verbose_name_plural = "School Years"
        
    def __unicode__(self):
        return self.name


class GraduationYear(core_mixins.DateTracking):
    year = models.PositiveSmallIntegerField("Graduation Year", unique=True)

    class Meta:
        verbose_name = "Graduation Year"
        verbose_name_plural = "Graduation Years"

    def __unicode__(self):
        return str(self.year)


class Language(core_mixins.DateTracking):
    name = models.CharField(max_length=42, unique=True, help_text="Maximum 42 characters")

    def __unicode__(self):
        return self.name
    
    
class Course(CommonInfo):
    name = models.CharField("Course Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    num = models.CharField("Course Number", max_length=10, help_text="Maximum 10 characters.")
    image = models.ImageField(upload_to=get_course_image_filename, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_course_thumbnail_filename, blank=True, null=True)
    sort_order = models.IntegerField("sort order", default=0, help_text='Courses will be ordered by the sort order. (Smallest at top.)')
    admin = models.CharField("Course Administrator", max_length=42, blank=True, null=True, help_text="Maximum 42 characters.")
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.num)
    
    class Meta:
        ordering = ['sort_order']
        
    

class EmploymentType(core_mixins.DateTracking):
    name = models.CharField("Employment Type", max_length = 42, unique = True, help_text="Maximum 42 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='EmploymentTypes will be ordered by the sort order. (Smallest at top.)')
   
    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"
        ordering = ['sort_order']

    def __unicode__(self):
        return self.name
        
    
class CampusOrgType(core_mixins.DateTracking):
    name = models.CharField("On-Campus Organization Type", max_length=42, unique=True, help_text="Maximum 42 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='CampusOrgTypes will be ordered by the sort order. (Smallest at top.)')
 
    class Meta:
        verbose_name = "On-Campus Organization Type"
        verbose_name_plural = "On-Campus Organization Types"
        ordering = ['sort_order']

    def __unicode__(self):
        return self.name
        
    
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


@receiver(signals.post_save, sender=CampusOrg)
@receiver(signals.post_save, sender=Course)
def create_recruiter_related_models(sender, instance, created, raw, **kwargs):
    if instance.image and not instance.thumbnail:
        temp_name, content = generate_thumbnail(instance.image)
        instance.thumbnail.save(temp_name, content)
        
class Industry(core_mixins.DateTracking):
    name = models.CharField("Industry Name", max_length=42, unique=True, help_text="Maximum 42 characters.")

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "Industries"
            
    def __unicode__(self):
        return self.name


class EventType(core_mixins.DateTracking):
    name = models.CharField("Event Type", max_length = 42, unique = True, help_text="Maximum 41 characters.")

    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
    
    def __unicode__(self):
        return self.name

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type('new_event', 'New Event', 'an employer has created a new event')
    notification.create_notice_type('public_invite', 'Public Event Invite', 'an employer has invited you to an event')
    notification.create_notice_type('private_invite', 'Private Event Invite', 'an employer has invited you to an event')

signals.post_syncdb.connect(create_notice_types, sender=notification)
