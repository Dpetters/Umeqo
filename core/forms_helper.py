"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from core.models import CampusOrgType, CampusOrg

def campus_org_types_as_choices():
    campus_org_types= []
    for campus_org_type in CampusOrgType.objects.all():
        campus_orgs = []
        for campus_org in CampusOrg.objects.filter(type = campus_org_type):
            campus_orgs.append([campus_org.id, campus_org.name])

        new_campus_org_type = [campus_org_type.name + "s", campus_orgs]
        campus_org_types.append(new_campus_org_type)

    return campus_org_types

from django.utils.html import escape

def add_required_label_tag(original_function):
    """Adds the 'required' CSS class and an asterisks to required field labels."""
    def required_label_tag(self, contents=None, attrs=None):
        contents = contents or escape(self.label)
        if self.field.required:
            attrs = {'class': 'required'}
        return original_function(self, contents, attrs)
    return required_label_tag

def decorate_bound_field():
    from django.forms.forms import BoundField  
    BoundField.label_tag = add_required_label_tag(BoundField.label_tag)