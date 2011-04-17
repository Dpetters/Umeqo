"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from django.db.models import Count

from core.models import CampusOrg, SchoolYear, GraduationYear, Course, UserProfile, Language, Industry
from core.models_helper import get_resume_filename
from employer.models import Employer
from events.models import Event


class Student(UserProfile):

    # Required Info
    first_name = models.CharField(max_length = 20, blank = True, null=True)
    last_name = models.CharField(max_length = 30, blank = True, null=True)
    school_year = models.ForeignKey(SchoolYear, blank = True, null=True)
    graduation_year = models.ForeignKey(GraduationYear, blank = True, null=True)
    first_major = models.ForeignKey(Course, related_name = "first_major", blank = True, null=True)
    gpa = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null=True)
    resume = models.FileField(upload_to = get_resume_filename, blank = True, null=True)
    
    # Basic Info
    older_than_18 = models.BooleanField()
    citizen = models.BooleanField()
    languages = models.ManyToManyField(Language, blank = True, null = True)
    website = models.URLField(blank = True, null=True)
    
    # Academic Info
    second_major = models.ForeignKey(Course, related_name = "second_major", blank = True, null=True)
    sat_t = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_m = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_v = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_w = models.PositiveSmallIntegerField(blank = True, null=True)
    act = models.PositiveSmallIntegerField(blank = True, null=True)
    
    #On-campus Involvement
    campus_orgs = models.ManyToManyField(CampusOrg, blank = True, null=True)

    # Work Info
    looking_for_internship = models.BooleanField()
    looking_for_fulltime = models.BooleanField()
    previous_employers = models.ManyToManyField(Employer, blank = True, null=True, related_name="previous_employers_of")
    industries_of_interest = models.ManyToManyField(Industry, blank = True, null=True, related_name="industries_of_interest_of")
    
    # Event Info
    subscribed_employers = models.ManyToManyField(Employer, blank = True, null=True, related_name="subscribed_employers")
    subscribed_industries = models.ManyToManyField(Industry, blank = True, null=True, related_name="subscribed_industries")
    last_seen_events = models.ManyToManyField(Event, blank = True, null=True, related_name = "last_seen_by")
    new_events = models.ManyToManyField(Event, blank = True, null = True)
    
    # Preferences
    email_on_invite_to_public_event = models.BooleanField()
    email_on_invite_to_private_event = models.BooleanField()
    email_on_new_event = models.BooleanField()
    
    # Statistics
    event_invite_count = models.PositiveIntegerField(editable=False, default = 0)
    add_to_resumebook_count = models.PositiveIntegerField(editable=False, default = 0)
    resume_view_count = models.PositiveIntegerField(editable=False, default = 0)
    shown_in_results_count = models.PositiveIntegerField(editable=False, default = 0)
    
    # Metadata
    profile_created = models.BooleanField(default=False)
    last_updated = models.DateTimeField(editable=False, blank = True, null=True)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    keywords = models.TextField()

    class Meta:
        verbose_name_plural = "Students"
    """
    def rank(self):
        aggregate = Student.objects.extra({'popularity':'invite_count*10+add_to_cart_count*5+resume_view_count*3 + results_count*1'}).aggregate(rank=Count('popularity'))
        return aggregate['rank']
    """
    """
    def __json__(self):
        json = { 'first_name' : self.first_name,
                 'last_name' : self.last_name,
                 'school_year' : self.school_year,
                 'graduation_year' : self.graduation_year,
                 'first_major' : {'display' : self.first_major.display,
                                  'num' : self.first_major.num,
                                  'name' : self.first_major.name},
                 'gpa' : str(self.gpa),
                 'resume' : str(self.resume),
                 'older_than_18' : self.older_than_18,
                 'citizen' : self.citizen,
                 'phone' : self.phone,
                 'languages' : self.languages,
                 'website' : self.website,
                 'sat_t' : str(self.sat_t),
                 'sat_m' : str(self.sat_m),
                 'sat_v' : str(self.sat_v),
                 'sat_w' : str(self.sat_w),
                 'act' : str(self.act),
                 'requires_sponsorship' : self.requires_sponsorship,
                 'looking_for_internship' : self.looking_for_internship,
                 'looking_for_fulltime' : self.looking_for_fulltime}
        
        campus_orgs = []
        for org in self.campus_org.all():
            campus_orgs.append({'display' : org.display,
                                 'name' : org.name,
                                 'type' : org.type})
        if campus_orgs:
            json['campus_orgs'] = campus_orgs
        
        employers = []
        for employer in self.previous_employers.all():
            employers.append({'name' : employer.company_name})
        if employers:
            json['employers'] = employers

        industries = []
        for industry in self.industries_of_interest.all():
            industries.append({'name' : industry.name})
        if industries:
            json['industries'] = industries
                    
        if self.second_major:
            json['second_major'] = {'display' : self.second_major.display,
                                   'num' : self.second_major.num,
                                   'name' : self.second_major.name}
        return json
    """
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
  
    def save( self, *args, **kwargs ):
        if self.first_name and self.last_name:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        super(Student, self).save( *args, **kwargs )