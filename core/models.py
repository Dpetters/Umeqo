"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
import Image, os
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from core.models_helper import get_image_filename
from core import enums

class Topic(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    sort_order = models.IntegerField(default=0, help_text='Topics will be ordered by the sort order. (Smallest at top.)')
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES)
    last_updated = models.DateTimeField(auto_now=True, default=datetime.now())
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now())
    
    class Meta:
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(Topic)
    status = models.IntegerField(choices=enums.QUESTION_STATUS_CHOICES, help_text="Only questions with their status set to 'Active' will be displayed." )
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES, default=enums.ALL)
    sort_order = models.IntegerField(default=0, help_text='Questions will be ordered by the sort order. (Smallest at top.)')
    question = models.TextField()
    answer = models.TextField() 
    slug = models.SlugField( max_length=100, help_text="This is a unique identifier that allows your questions to display its detail view, ex 'how-can-i-contribute'", )
    last_updated = models.DateTimeField(auto_now=True, default=datetime.now())
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now())

    class Meta:
        ordering = ['sort_order', 'question']
        
    def __unicode__(self):
        return self.question
        
         
class CommonInfo(models.Model):
    email = models.EmailField("Contact E-mail", blank=True, null=True)
    website = models.URLField(blank=True, null=True, verify_exists=False)
    description = models.TextField(max_length=500, blank=True, null=True, help_text="Maximum 500 characters.")
    image = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    display = models.BooleanField(help_text="Only select if all of the above info has been checked for errors and finalized.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
 
 
class SchoolYear(models.Model):
    name = models.CharField("School Year", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "School Year"
        verbose_name_plural = "School Years"
        
    def __unicode__(self):
        return self.name


class Ethnicity(models.Model):
    name = models.CharField("Ethnicity", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ethnicity"
        verbose_name_plural = "Ethnicities"
        
    def __unicode__(self):
        return self.name

    
class GraduationYear(models.Model):
    year = models.PositiveSmallIntegerField("Graduation Year", unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Graduation Year"
        verbose_name_plural = "Graduation Years"

    def __unicode__(self):
        return str(self.year)


class Language(models.Model):
    name = models.CharField(max_length=42, unique=True, help_text="Maximum 42 characters")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    def __unicode__(self):
        return self.name
    
    
class Course(CommonInfo):
    name = models.CharField("Course Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    num = models.CharField("Course Number", max_length=10, help_text="Maximum 10 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='Courses will be ordered by the sort order. (Smallest at top.)')
    admin = models.CharField("Course Administrator", max_length=42, blank=True, null=True, help_text="Maximum 42 characters.")
    
    class Meta:
        ordering = ['sort_order']
        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.num)
    
    def save(self, *args, **kwargs):
        old_instance = Course.objects.get(id=self.id)
        if old_instance.image:
            os.remove(old_instance.image.path)
        self.full_clean()
        super(Course, self).save(*args, **kwargs)


class EmploymentType(models.Model):
    name = models.CharField("Employment Type", max_length = 42, unique = True, help_text="Maximum 42 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='EmploymentTypes will be ordered by the sort order. (Smallest at top.)')
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"
        ordering = ['sort_order']

    def __unicode__(self):
        return self.name
        
    
class CampusOrgType(models.Model):
    name = models.CharField("On-Campus Organization Type", max_length=42, unique=True, help_text="Maximum 42 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='CampusOrgTypes will be ordered by the sort order. (Smallest at top.)')
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "On-Campus Organization Type"
        verbose_name_plural = "On-Campus Organization Types"
        ordering = ['sort_order']

    def __unicode__(self):
        return self.name
        
    
class CampusOrg(CommonInfo):
    name = models.CharField("On-Campus Organization Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    type = models.ForeignKey(CampusOrgType)

    class Meta(CommonInfo.Meta):
        verbose_name = "On-Campus Organization"
        verbose_name_plural = "On-Campus Organizations"

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        old_instance = CampusOrg.objects.get(id=self.id)
        if old_instance.image:
            os.remove(old_instance.image.path)
        self.full_clean()
        super(CampusOrg, self).save(*args, **kwargs)
             

class Industry(models.Model):
    name = models.CharField("Industry Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "Industries"
            
    def __unicode__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField("Event Type", max_length = 42, unique = True, help_text="Maximum 41 characters.")
    last_updated = models.DateTimeField(auto_now = True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
    
    def __unicode__(self):
        return self.name


@receiver(signals.post_save, sender=CampusOrg)
@receiver(signals.post_save, sender=Course)
def resize_image(sender, instance, **kwargs):
    if instance.image:
        filename = instance.image.path
        image = Image.open(filename)
        ratio = min(float(settings.MAX_DIALOG_IMAGE_WIDTH)/instance.image.width, float(settings.MAX_DIALOG_IMAGE_HEIGHT)/instance.image.height)
        size = (int(ratio * instance.image.width), int(ratio * instance.image.height))
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)