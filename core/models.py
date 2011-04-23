"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.db import models
from django.contrib.auth.models import User

from core.models_helper import get_image_filename

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
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(EmploymentType, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
class CampusOrgType(models.Model):
    name = models.CharField("On-Campus Organization Type", max_length=42, unique=True, help_text="Maximum 42 characters.")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "On-Campus Organization Type"
        verbose_name_plural = "On-Campus Organization Types"
    
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
        
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    
    class Meta:
        abstract = True,
        ordering = ['user']
