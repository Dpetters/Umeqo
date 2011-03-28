"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.contrib import admin

from employer.models import Employer

class EmployerAdmin(admin.ModelAdmin):
    fields = ['user', 'company_name', 'industries', 'contact_phone']
    list_display = ('company_name', 'user', 'contact_phone')
    search_fields = ['company_name', 'industries__name']
    date_hierarchy = 'date_created'
    
admin.site.register(Employer, EmployerAdmin)