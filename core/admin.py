"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import InterestedPerson, CampusOrgType, CampusOrg, Course, Language, SchoolYear, GraduationYear, Industry

class InterestedPersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(InterestedPerson, InterestedPersonAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('groups','is_active', 'is_staff')
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'date_joined'

class IndustryAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
    
class SchoolYearAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)

class GraduationYearAdmin(admin.ModelAdmin):
    fields = ['year']
    ordering = ('-year',)

class LanguageAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
    
class CampusOrgTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    ordering = ('-last_updated',)
    date_hierarchy = 'last_updated'
    
class CampusOrgAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['name', 'type']}),
        ('Extra Info', {'fields': ['email', 'website', 'image', 'description', 'display']}),
    ]
    list_display = ('name', 'type', 'display')
    list_filter = ('type',)
    search_fields = ['name']
    date_hierarchy = 'last_updated'


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Required Info', {'fields': ['name', 'num']}),
        ('Extra Content', {'fields': ['admin', 'email', 'website', 'image', 'description', 'display']}),
    ]
    list_display = ('name', 'num', 'display')
    search_fields = ['name']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(GraduationYear, GraduationYearAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CampusOrgType, CampusOrgTypeAdmin)
admin.site.register(CampusOrg, CampusOrgAdmin)