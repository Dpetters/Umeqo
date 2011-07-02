"""
 Developers : Joshua Ma,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from datetime import datetime
from employer.models import Employer
from haystack import indexes, site

class EmployerIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    content_auto = indexes.EdgeNgramField(use_template=True)
    industries = indexes.MultiValueField()
    has_events = indexes.BooleanField()

    def prepare_industries(self, obj):
        return [industry.id for industry in obj.industries.all()]
    
    def prepare_has_events(self, obj):
        recruiters = obj.recruiter_set.all()
        for recruiter in recruiters:
            if recruiter.event_set.filter(end_datetime__gte=datetime.now()).count() > 0:
                return True
        return False

site.register(Employer, EmployerIndex)
