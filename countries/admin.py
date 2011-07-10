from django.contrib import admin

from countries.models import Country

class CountryAdmin(admin.ModelAdmin):
    pass
        
admin.site.register(Country, CountryAdmin)