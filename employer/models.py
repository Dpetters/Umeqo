from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models import signals

from student.models import Student
from core import choices
from core.models import Industry, EmploymentType, SchoolYear, GraduationYear, Course
from employer import enums as employer_enums
from employer.model_helpers import get_resume_book_filename, get_logo_filename
from student.models import StudentBaseAttributes
from core import mixins as core_mixins


class Employer(core_mixins.DateTracking): 
    name = models.CharField(max_length = 42, unique = True, help_text="Maximum 42 characters.")
    description = models.CharField(max_length=500)
    logo = models.ImageField(upload_to=get_logo_filename)
    slug = models.CharField(max_length=20, unique=True, help_text="Maximum 20 characters.")
    offered_job_types = models.ManyToManyField(EmploymentType, blank = True, null=True) 
    industries = models.ManyToManyField(Industry)

    main_contact = models.CharField("Main Contact", max_length = 50)
    main_contact_email = models.EmailField("Contact Email")
    main_contact_phone = PhoneNumberField("Contact Phone #")

    def __unicode__(self):
        return self.name

@receiver(signals.post_save, sender=Employer)
def create_employer_related_models(sender, instance, created, raw, **kwargs):
    if created:
        if not EmployerStatistics.objects.filter(employer=instance).exists():
            EmployerStatistics.objects.create(employer=instance)


class EmployerStatistics(core_mixins.DateTracking):
    employer = models.OneToOneField(Employer, unique=True, editable=False)
    
    resumes_viewed = models.PositiveIntegerField(default = 0, editable=False, blank = True, null=True)

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
    starred_students = models.ManyToManyField("student.Student")

    def __unicode__(self):
        if hasattr(self, "user"):
            return str(self.user)
        else:
            return "Unattached Recruiter"

@receiver(signals.post_save, sender=Recruiter)
def create_recruiter_related_models(sender, instance, created, raw, **kwargs):
    if created:
        if not RecruiterPreferences.objects.filter(recruiter=instance).exists():
            RecruiterPreferences.objects.create(recruiter=instance)
        if not RecruiterStatistics.objects.filter(recruiter=instance).exists():
            RecruiterStatistics.objects.create(recruiter=instance)


class ResumeBook(core_mixins.DateTracking):
    recruiter = models.ForeignKey("employer.Recruiter", editable=False)
    resume_book = models.FileField(upload_to = get_resume_book_filename, blank = True, null=True)
    name = models.CharField("Resume Book Name", max_length = 42, blank = True, null = True, help_text="Maximum 42 characters.")
    students = models.ManyToManyField("student.Student", blank = True, null = True)

    def __unicode__(self):
        return self.name


class DefaultStudentFilteringParams(StudentBaseAttributes, core_mixins.DateTracking):
    recruiter = models.OneToOneField(Recruiter, unique=True, editable=False)

    majors = models.ManyToManyField(Course, blank = True, null = True)    
    school_years = models.ManyToManyField(SchoolYear, blank = True, null = True)
    graduation_years = models.ManyToManyField(GraduationYear, blank = True, null = True)

    employment_types = models.ManyToManyField(EmploymentType, blank = True, null = True)
    
    older_than_21 = models.CharField(max_length=1, choices = choices.NO_YES_CHOICES, blank = True, null = True)


class StudentComment(models.Model):
    recruiter = models.ForeignKey(Recruiter)
    student = models.ForeignKey(Student)
    comment = models.CharField(max_length=500)
    
    class Meta:
        unique_together = (("recruiter", "student"),)

        
class RecruiterPreferences(core_mixins.DateTracking):
    recruiter = models.OneToOneField(Recruiter, unique=True, editable=False)
    
    email_on_rsvp = models.BooleanField()
    results_per_page = models.PositiveSmallIntegerField(choices=employer_enums.RESULTS_PER_PAGE_CHOICES, default=10)
    default_student_ordering = models.CharField(max_length = 42, choices=employer_enums.ORDERING_CHOICES, default=employer_enums.ORDERING_CHOICES[0][0])

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
     
    resumes_viewed = models.PositiveIntegerField(default = 0, editable=False, blank = True, null=True)

    class Meta:
        verbose_name = "Recruiter Statistics"
        verbose_name_plural = "Recruiter Statistics"

    def __unicode__(self):
        if hasattr(self, "recruiter"):
            return "Recruiter Statistics for %s" % (self.recruiter,)
        else:
            return "Unattached Recruiter Statistics"