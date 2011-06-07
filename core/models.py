"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from datetime import datetime
 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from core.models_helper import get_image_filename
from core import enums

class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    sort_order = models.IntegerField(_('sort order'), default=0, help_text='The order you would like the topic to be displayed.')
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES)
    
    class Meta:
        ordering = ['sort_order', 'name']

    def __unicode__(self):
        return self.name


class Question(models.Model):
    """
    Represents a frequently asked question.
    """
    topic = models.ForeignKey(Topic)    
    status = models.IntegerField( choices=enums.QUESTION_STATUS_CHOICES, help_text="Only questions with their status set to 'Active' will be displayed." )
    audience = models.IntegerField(choices = enums.TOPIC_AUDIENCE_CHOICES, default=enums.ALL)
    sort_order = models.IntegerField(_('sort order'), default=0, help_text='This in which you would like the question to be displayed.')
    
    question = models.TextField(_('question'))
    answer = models.TextField( _('answer')) 
    
    slug = models.SlugField( max_length=100, help_text="This is a unique identifier that allows your questions to display its detail view, ex 'how-can-i-contribute'", )

    created_by = models.ForeignKey(User, null=True, editable=False, related_name="%(class)s_created" )    
    created_on = models.DateTimeField( _('created on'), default=datetime.now, editable=False)
    updated_on = models.DateTimeField( _('updated on'), editable=False)
    updated_by = models.ForeignKey(User, null=True, editable=False, related_name="%(class)s_updated" )
    
    class Meta:
        ordering = ['sort_order', 'created_on']

    def __unicode__(self):
        return self.question

    def save(self, *args, **kwargs):
        self.updated_on = datetime.now()
        super(Question, self).save(*args, **kwargs)
        
         
class CommonInfo(models.Model):
    email = models.EmailField("Contact E-mail", blank=True, null=True)
    website = models.URLField(blank=True, null=True, verify_exists=False)
    description = models.TextField(max_length=500, blank=True, null=True, help_text="Maximum 500 characters.")
    image = models.ImageField(upload_to=get_image_filename, blank=True, null=True, help_text="Resize to 240 x 160 before uploading.")
    display = models.BooleanField(help_text="Only select if all of the above info has been checked for errors and finalized.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name
 
 
class SchoolYear(models.Model):
    name = models.CharField("School Year", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "School Year"
        verbose_name_plural = "School Years"
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(SchoolYear, self).save(*args, **kwargs)


class Ethnicity(models.Model):
    name = models.CharField("Ethnicity", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ethnicity"
        verbose_name_plural = "Ethnicities"
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Ethnicity, self).save(*args, **kwargs)

    
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
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Language, self).save(*args, **kwargs)
    
    
class Course(CommonInfo):
    name = models.CharField("Course Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    num = models.CharField("Course Number", max_length=10, help_text="Maximum 10 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='The order you would like the majors to be displayed.')
    admin = models.CharField("Course Administrator", max_length=41, blank=True, null=True, help_text="Maximum 43 characters.")
    
    def __unicode__(self):
        return self.name + " (" + self.num + ")"
    
    class Meta:
        ordering = ['sort_order']

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Course, self).save(*args, **kwargs)

class EmploymentType(models.Model):
    name = models.CharField("Employment Type", max_length = 42, unique = True)
    sort_order = models.IntegerField("sort order", default=0, help_text='The order you would like the employment types to be displayed.')
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"
        ordering = ['sort_order']
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(EmploymentType, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
    
class CampusOrgType(models.Model):
    name = models.CharField("On-Campus Organization Type", max_length=42, unique=True, help_text="Maximum 42 characters.")
    sort_order = models.IntegerField("sort order", default=0, help_text='The order you would like the campus org types to be displayed.')
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "On-Campus Organization Type"
        verbose_name_plural = "On-Campus Organization Types"
        ordering = ['sort_order']
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(CampusOrgType, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
    
class CampusOrg(CommonInfo):
    name = models.CharField("On-Campus Organization Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    type = models.ForeignKey(CampusOrgType)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CampusOrg, self).save(*args, **kwargs)
           
    class Meta(CommonInfo.Meta):
        verbose_name = "On-Campus Organization"
        verbose_name_plural = "On-Campus Organizations"

        
class Industry(models.Model):
    name = models.CharField("Industry Name", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Industry, self).save(*args, **kwargs)
        
    class Meta(CommonInfo.Meta):
        verbose_name_plural = "Industries"

class EventType(models.Model):
    name = models.CharField("Event Type", max_length = 42, unique = True, help_text="Maximum 41 characters.")
    last_updated = models.DateTimeField(auto_now = True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(EventType, self).save(*args, **kwargs)