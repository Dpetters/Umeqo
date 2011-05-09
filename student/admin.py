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
    fields = ['name', 'employers', 'event', 'type', 'sort_order', 'students']
    list_display = ('name', 'type')
    
admin.site.register(StudentList, StudentListAdmin)
admin.site.register(Student, StudentAdmin)