"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.contrib import admin

from employer.models import Employer, Recruiter

class RecruiterAdmin(admin.ModelAdmin):
    fields = ['user', 'employer', 'is_active']
    list_display = ('employer', 'is_active', 'subscribed', 'date_created')
    search_fields = ['employer']
    date_hierarchy = 'date_created'
        
admin.site.register(Recruiter, RecruiterAdmin)
    
class EmployerAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'industries', 'main_contact', 'main_contact_phone']
    list_display = ('name', 'main_contact', 'main_contact_phone', 'date_created')
    search_fields = ['name', 'industries__name', 'main_contact']
    date_hierarchy = 'date_created'
    
admin.site.register(Employer, EmployerAdmin)