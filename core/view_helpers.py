from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q

from campus_org.models import CampusOrg
from employer.models import Employer
from core.decorators import is_student, is_recruiter, is_campus_org
from core import enums

def filter_faq_questions(user, questions):
    if is_recruiter(user):
        questions = questions.filter(Q(audience = enums.ANONYMOUS_AND_EMPLOYERS) | Q(audience=enums.CAMPUS_ORGS_AND_EMPLOYERS) | Q(audience=enums.EMPLOYER) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
    elif is_student(user):
        questions = questions.filter(Q(audience = enums.ANONYMOUS_AND_STUDENTS) | Q(audience=enums.STUDENT) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))
    elif is_campus_org(user):
        questions = questions.filter(Q(audience = enums.ANONYMOUS_AND_CAMPUS_ORGS) | Q(audience=enums.CAMPUS_ORGS_AND_EMPLOYERS) | Q(audience=enums.CAMPUS_ORG) | Q(audience=enums.AUTHENTICATED) | Q(audience=enums.ALL))            
    else:
        questions = questions.filter(Q(audience = enums.ANONYMOUS_AND_CAMPUS_ORGS) | Q(audience = enums.ANONYMOUS_AND_EMPLOYERS) | Q(audience = enums.ANONYMOUS_AND_STUDENTS) | Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
    return questions

def employer_campus_org_slug_exists(slug, campusorg=None, employer=None):
    try:
        existing_campusorg = CampusOrg.objects.get(slug=slug)
        if existing_campusorg==campusorg:
            return False
        return True
    except CampusOrg.DoesNotExist:
        pass
    try:
        existing_employer = Employer.objects.get(slug=slug)
        if existing_employer==employer:
            return False
        return True
    except Employer.DoesNotExist:
        pass
    return False

def does_email_exist(email):
    try:
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False

def english_join(l):
    if len(l) == 1:
        return str(l[0])
    if len(l) == 2:
        return '%s and %s' % (l[0], l[1])
        return ' and '.join(l)
    if len(l) > 2:
        o = ''
        for i,x in zip(range(len(l)), l):
            item = str(l[i])
            if i == len(l)-1:
                o += ', and '
            elif i > 0:
                o += ', '
            o += item
        return o

def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR'].split(',')[-1]
    elif 'REMOTE_ADDR' in request.META:
        return request.META['REMOTE_ADDR']
    else:
        return None

def um_slugify(s):
    parts = filter(lambda n: n not in ('the', 'a', 'an', 'of', 'for'), s.split(' '))
    new_s = ' '.join(parts)
    if len(new_s) > 50:
        parts = new_s.split(' ')
        new_len, new_parts, i = 0, [], 0
        while new_len < 40:
            new_parts.append(parts[i])
            new_len += len(parts[i])
            i += 1
        new_s = ' '.join(new_parts)
    return slugify(new_s)
