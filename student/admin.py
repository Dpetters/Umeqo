"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.contrib import admin

from student.models import StudentList, Student

class StudentAdmin(admin.ModelAdmin):
    pass

class StudentListAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(StudentList, StudentListAdmin)
admin.site.register(Student, StudentAdmin)