"""
 Developers : Joshua Ma,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from haystack import indexes, site
from employer.models import Employer

class EmployerIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    content_auto = indexes.EdgeNgramField(use_template=True)

site.register(Employer, EmployerIndex)
