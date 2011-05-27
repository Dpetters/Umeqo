"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.contrib import admin

from relationships.models import Relationship

class RelationshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(Relationship, RelationshipAdmin)
