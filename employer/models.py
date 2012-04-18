from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from core import choices, mixins as core_mixins
from core.models import Industry, EmploymentType, SchoolYear, GraduationYear, Course
from employer import enums as employer_enums
from employer.model_helpers import get_resume_book_filename, get_logo_filename
from student.models import Student, StudentBaseAttributes
from employer.managers import EmployerManager
from subscription.choices import EMPLOYER_SIZE_CHOICES
from subscription.models import EmployerSubscription


class Employer(core_mixins.DateTracking): 
    # Mandatory Fields
    name = models.CharField(max_length=42, unique=True, help_text="Maximum 42 characters.")
    slug = models.SlugField(max_length=20, help_text="Maximum 20 characters.", null=True, blank=True)
    logo = models.ImageField(upload_to=get_logo_filename, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    industries = models.ManyToManyField(Industry, null=True, blank=True)
    visible = models.BooleanField(default=False)
    
    # Null Fields
    offered_job_types = models.ManyToManyField(EmploymentType, blank=True, null=True) 
    size = models.CharField("Firm Size", choices = EMPLOYER_SIZE_CHOICES, max_length = 20, blank=True, null=True)
    careers_website = models.URLField(verify_exists=False, blank=True, null=True)
    starred_students = models.ManyToManyField("student.Student", blank=True, null=True)
    
    stripe_id = models.CharField(max_length=255, null=True, blank=True)
  
    objects = EmployerManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering=["name"]
           
    def get_absolute_url(self):
        return '%s?id=%d' % (reverse('employers'), self.id)
    
    def has_basic(self):
        try:
            subscription = self.employersubscription
        except EmployerSubscription.DoesNotExist:
            return False
        else:
            if subscription.basic_subscription() and not subscription.expired():
                return True
        return False

    def has_premium(self):
        try:
            subscription = self.employersubscription
        except EmployerSubscription.DoesNotExist:
            return False
        else:
            if subscription.premium_subscription() and not subscription.expired():
                return True
        return False
        
                
@receiver(signals.post_save, sender=Employer)
def create_employer_related_models(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if not EmployerStatistics.objects.filter(employer=instance).exists():
            EmployerStatistics.objects.create(employer=instance)


class EmployerStatistics(core_mixins.DateTracking):
    employer = models.OneToOneField(Employer, unique=True, editable=False)
    resumes_viewed = models.PositiveIntegerField(default=0, editable=False, blank=True, null=True)

    class Meta:
        verbose_name = "Employer Statistics"
        verbose_name_plural = "Employer Statistics"

    def __unicode__(self):
        if hasattr(self, "employer"):
            return "Employer Statistics for %s" % (self.employer,)
        else:
            return "Unattached Employer Statistics"


class Recruiter(core_mixins.DateTracking):
    user = models.OneToOneField(User, unique=True)
    employer = models.ForeignKey("employer.Employer")

    def __unicode__(self):
        if hasattr(self, "user"):
            return str(self.user)
        else:
            return "Unattached Recruiter"
    class Meta:
        ordering=["user__first_name"]
        
@receiver(signals.post_save, sender=Recruiter)
def create_recruiter_related_models(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if not RecruiterPreferences.objects.filter(recruiter=instance).exists():
            RecruiterPreferences.objects.create(recruiter=instance)
        if not RecruiterStatistics.objects.filter(recruiter=instance).exists():
            RecruiterStatistics.objects.create(recruiter=instance)


class ResumeBook(core_mixins.DateTracking):
    recruiter = models.ForeignKey("employer.Recruiter", editable=False)
    resume_book = models.FileField(upload_to=get_resume_book_filename, blank=True, null=True)
    name = models.CharField("Resume Book Name", max_length=42, blank=True, null=True, help_text="Maximum 42 characters.")
    students = models.ManyToManyField("student.Student", blank=True, null=True)
    delivered = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return "Resume Book"

    class Meta:
        ordering = ['-last_updated']
        verbose_name = "Resume Book"
        verbose_name_plural = "Resume Books"
        
class StudentFilteringParameters(StudentBaseAttributes, core_mixins.DateTracking):
    recruiter = models.OneToOneField(Recruiter, unique=True, editable=False)
    majors = models.ManyToManyField(Course, blank=True, null=True)    
    school_years = models.ManyToManyField(SchoolYear, blank=True, null=True)
    graduation_years = models.ManyToManyField(GraduationYear, blank=True, null=True)
    employment_types = models.ManyToManyField(EmploymentType, blank=True, null=True)
    older_than_21 = models.CharField(max_length=1, choices=choices.NO_YES_CHOICES, blank=True, null=True)


class EmployerStudentComment(core_mixins.DateTracking):
    employer = models.ForeignKey(Employer)
    student = models.ForeignKey(Student)
    comment = models.CharField(max_length=500)
    
    class Meta:
        verbose_name = "Employer Student Comment"
        verbose_name_plural = "Employer Student Comments"
        unique_together = (("employer", "student"),)

        
class RecruiterPreferences(core_mixins.DateTracking):
    recruiter = models.OneToOneField(Recruiter, unique=True, editable=False)
    
    email_on_rsvp_to_public_event = models.BooleanField()
    email_on_rsvp_to_private_event = models.BooleanField()
    default_student_results_per_page = models.PositiveSmallIntegerField(choices=employer_enums.RESULTS_PER_PAGE_CHOICES, default=10)
    default_student_result_ordering = models.CharField(max_length=42, choices=employer_enums.ORDERING_CHOICES, default=employer_enums.ORDERING_CHOICES[0][0])

    class Meta:
        verbose_name = "Recruiter Preferences"
        verbose_name_plural = "Recruiter Preferences"
    
    def __unicode__(self):
        if hasattr(self, "recruiter"):
            return "Recruiter Preferences for %s" % (self.recruiter,)
        else:
            return "Unattached Recruiter Preferences"


class RecruiterStatistics(core_mixins.DateTracking):
    recruiter = models.OneToOneField(Recruiter, unique=True, editable=False)
    resumes_viewed = models.PositiveIntegerField(default=0, editable=False, blank=True, null=True)

    class Meta:
        verbose_name = "Recruiter Statistics"
        verbose_name_plural = "Recruiter Statistics"

    def __unicode__(self):
        if hasattr(self, "recruiter"):
            return "Recruiter Statistics for %s" % (self.recruiter,)
        else:
            return "Unattached Recruiter Statistics"