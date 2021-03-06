import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from countries.models import Country
from campus_org.models import CampusOrg
from core.models import SchoolYear, GraduationYear, Course, Language, Industry, EmploymentType, School
from core.model_helpers import get_resume_filename
from core import choices as core_choices
from core import mixins as core_mixins
from student.managers import StudentManager

class DegreeProgram(core_mixins.DateTracking):
    name = models.CharField("Degree Program", max_length=42, unique=True, help_text="Maximum 42 characters.")
    name_plural = models.CharField("Degree Program Verbose", max_length=43, unique=True, help_text="Maximum 42 characters.", null=True)
    sort_order = models.FloatField(help_text='Topics will be ordered by the sort order. (Smallest at top.)', default=0)
    
    class Meta:
        verbose_name = "Degree Program"
        verbose_name_plural = "Degree Programs"
        ordering = ['sort_order']
        
    def __unicode__(self):
        return self.name

class StudentInvite(core_mixins.DateTracking):
    code = models.CharField(max_length=12, unique=True)
    used = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s" % (self.code)
    
    class Meta:
        verbose_name = "Student Invite"
        verbose_name_plural = "Student Invites"


class StudentBaseAttributes(models.Model):
    previous_employers = models.ManyToManyField('employer.Employer', blank = True, null=True, symmetrical=False)
    industries_of_interest = models.ManyToManyField(Industry, blank = True, null=True)
    gpa = models.FloatField(blank = True, null=True)    
    sat_t = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_m = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_v = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_w = models.PositiveSmallIntegerField(blank = True, null=True)
    act = models.PositiveSmallIntegerField(blank = True, null=True)
        
    campus_involvement = models.ManyToManyField(CampusOrg, blank = True, null = True)
    languages = models.ManyToManyField(Language, blank = True, null = True)
    countries_of_citizenship = models.ManyToManyField(Country, blank=True, null=True)
    
    class Meta:
        abstract = True


class Student(StudentBaseAttributes, core_mixins.DateCreatedTracking):
    user = models.OneToOneField(User, unique=True)
    profile_created = models.BooleanField(default=False)
    
    keywords = models.TextField(blank=True, null=True)
    first_name = models.CharField(db_index = True, max_length = 20, blank = True, null=True)
    last_name = models.CharField(max_length = 30, blank = True, null=True)
    degree_program = models.ForeignKey(DegreeProgram, blank = True, null = True)
    graduation_year = models.ForeignKey(GraduationYear, blank = True, null=True)
    graduation_month = models.CharField(max_length=2, choices = core_choices.MONTH_CHOICES, default = core_choices.JUNE, blank = True, null = True)
    first_major = models.ForeignKey(Course, related_name = "first_major", blank = True, null=True)
    resume = models.FileField(upload_to = get_resume_filename, blank = True, null=True)
    
    second_major = models.ForeignKey(Course, related_name = "second_major", blank = True, null=True)
    looking_for = models.ManyToManyField(EmploymentType, blank = True, null=True) 
    
    website = models.URLField(verify_exists=False, blank = True, null=True)
    older_than_21 = models.CharField(max_length=1, choices = core_choices.SELECT_YES_NO_CHOICES, blank = True, null = True)
    
    last_updated = models.DateTimeField(editable=False, default=datetime.datetime.now())
    
    subscriptions = models.ManyToManyField("employer.Employer", blank=True, null=True, related_name="subscribers")
    
    objects = StudentManager()
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def __unicode__(self):
        if hasattr(self, "user"):
            return str(self.user)
        else:
            return "Unattached Student"

    def deactivate(self):
        self.user.is_active = False
        self.user.save()
        
    def suspend(self):
        self.user.userattributes.is_verified = False
        self.user.userattributes.save()
        self.user.is_active = False
        self.user.save()
    
    def visible(self):
        return (self.user.is_active and self.user.userattributes.is_verified and self.profile_created)

@receiver(post_save, sender=Student)
def create_student_related_models(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.first_name and instance.last_name:
            instance.user.first_name = instance.first_name
            instance.user.last_name = instance.last_name
            instance.user.save()
        StudentPreferences.objects.create(student=instance)
        StudentStatistics.objects.create(student=instance)


class StudentDeactivation(core_mixins.DateCreatedTracking):
    student = models.ForeignKey("student.Student")
    suggestion = models.CharField(max_length=16384, null=True, blank=True)

    class Meta:
        verbose_name = "Student Deactivation"
        verbose_name_plural = "Student Deactivations"
    
    def __unicode__(self):
        return "%s's Deactivation" % (str(self.student))


class StudentPreferences(core_mixins.DateTracking):
    student = models.OneToOneField("student.Student", unique=True, editable=False)
    
    email_on_invite_to_public_event = models.BooleanField(default=True)
    email_on_invite_to_private_event = models.BooleanField(default=True)
    email_on_new_subscribed_employer_event = models.BooleanField(default=True)
    receive_monthly_newsletter = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Student Preferences"
        verbose_name_plural = "Student Preferences"
    
    def __unicode__(self):
        if hasattr(self, "student"):
            return "Student Preferences for %s" % (self.student,)
        else:
            return "Unattached Student Preferences"


class StudentStatistics(core_mixins.DateTracking):
    student = models.OneToOneField("student.Student", unique=True, editable=False)
    
    add_to_resumebook_count = models.PositiveIntegerField(editable=False, default = 0)
    resume_view_count = models.PositiveIntegerField(editable=False, default = 0)
    shown_in_results_count = models.PositiveIntegerField(editable=False, default = 0)
    raffles_won = models.PositiveIntegerField(editable=False, default = 0)
    
    class Meta:
        verbose_name = "Student Statistics"
        verbose_name_plural = "Student Statistics"

    def __unicode__(self):
        if hasattr(self, "student"):
            return "Student Statistics for %s" % (self.student,)
        else:
            return "Unattached Student Statistics"
