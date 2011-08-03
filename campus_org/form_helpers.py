from core.models import CampusOrgType
from campus_org.models import CampusOrg

def campus_org_types_as_choices():
    campus_org_types= []
    for campus_org_type in CampusOrgType.objects.all():
        campus_orgs = []
        for campus_org in CampusOrg.objects.filter(type = campus_org_type):
            campus_orgs.append([campus_org.id, campus_org.name])
        if campus_orgs:
            new_campus_org_type = [campus_org_type.name, campus_orgs]
            campus_org_types.append(new_campus_org_type)
    return campus_org_types
