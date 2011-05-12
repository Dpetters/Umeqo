"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from haystack import indexes, site
from student.models import Student

class StudentIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)

site.register(Student, StudentIndex)
