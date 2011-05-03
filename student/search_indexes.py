"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from haystack import indexes, site
from student.models import Student

class StudentIndex(indexes.RealTimeSearchIndex):
    keywords = indexes.CharField(use_template=True, document=True)
    first_name = indexes.CharField(model_attr="first_name", null=True)
    last_name = indexes.CharField(model_attr="last_name", null=True)

site.register(Student, StudentIndex)
