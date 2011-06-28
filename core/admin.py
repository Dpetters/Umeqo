"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Ethnicity, CampusOrgType, CampusOrg, Course, Language, SchoolYear, GraduationYear, Industry, Topic, Question, EmploymentType

class EthnicityAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)

admin.site.register(Ethnicity, EthnicityAdmin)

class TopicAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'sort_order', 'audience')
    list_filter = ['audience']
    search_fields = ['name']
    
class QuestionAdmin(admin.ModelAdmin):
    fields= ['audience', 'status', 'sort_order', 'question', 'answer', 'slug']
    prepopulated_fields = {'slug':('question',)}
    list_display = ['question', 'topic', 'audience', 'sort_order', 'status']
    list_filter = ['topic', 'audience', 'status']
    search_fields = ['question', 'answer']
    
    def save_model(self, request, obj, form, change): #@UnusedVariable
        '''
        Overrided because I want to also set who created this instance.
        '''
        instance = form.save( commit=False )
        if instance.id is None:
            instance.created_by = request.user
                
        instance.updated_by = request.user
        instance.save()
        
        return instance

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
    
class EmploymentTypeAdmin(admin.ModelAdmin):
    fields = ['name', 'sort_order']
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
admin.site.register(EmploymentType, EmploymentTypeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)