from haystack import indexes, site
from student.models import Student

class StudentIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)

site.register(Student, StudentIndex)
