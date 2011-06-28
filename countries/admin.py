"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.contrib import admin

from countries.models import Country

class CountryAdmin(admin.ModelAdmin):
    pass
        
admin.site.register(Country, CountryAdmin)