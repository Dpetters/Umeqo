from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from campus_org.models import CampusOrg
from employer.models import Employer
from core.decorators import is_student, is_recruiter, is_campus_org
from core import enums as core_enums

def search(sqs, query):
    or_terms = map(lambda x: x.strip(), query.split("OR"))
    print or_terms
    for i, query in enumerate(or_terms):
        # Pull out anything wrapped in quotes and do an exact match on it.
        open_quote_position = None
        non_exact_query = query
        print query
        for offset, char in enumerate(query):
            if char == '"':
                if open_quote_position != None:
                    current_match = non_exact_query[open_quote_position + 1:offset]
    
                    if current_match:
                        print sqs.query.clean(current_match)
                        sqs = sqs.filter(text__exact=sqs.query.clean(current_match))
    
                    non_exact_query = non_exact_query.replace('"%s"' % current_match, '', 1)
                    open_quote_position = None
                else:
                    open_quote_position = offset
        
        # Pseudo-tokenize the rest of the query.
        keywords = non_exact_query.split()
        
        # Loop through keywords and add filters to the query.
        for keyword in keywords:
            exclude = False
            
            if keyword.startswith('-') and len(keyword) > 1:
                keyword = keyword[1:]
                exclude = True
            
            cleaned_keyword = sqs.query.clean(keyword)
            
            if exclude:
                sqs = sqs.exclude(content=cleaned_keyword)
            else:
                if i==0:
                    sqs = sqs.filter(text=cleaned_keyword)                
                else:
                    sqs = sqs.filter_or(text=cleaned_keyword)
    
    return sqs

def get_audiences(user):
    if is_student(user):
        return [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_STUDENTS, core_enums.STUDENT]
    elif is_recruiter(user):
        return [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_EMPLOYERS, core_enums.EMPLOYER, core_enums.CAMPUS_ORGS_AND_EMPLOYERS]
    elif is_campus_org(user):
        return [core_enums.ALL, core_enums.AUTHENTICATED, core_enums.ANONYMOUS_AND_CAMPUS_ORGS, core_enums.CAMPUS_ORG, core_enums.CAMPUS_ORGS_AND_EMPLOYERS]
    else:
        return [core_enums.ALL, core_enums.ANONYMOUS, core_enums.ANONYMOUS_AND_CAMPUS_ORGS, core_enums.ANONYMOUS_AND_EMPLOYERS, core_enums.ANONYMOUS_AND_STUDENTS]

def filter_faq_questions(user, questions):
    return questions.filter(audience__in = get_audiences(user))

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
    new_s = slugify(' '.join(parts))
    if len(new_s) > 50:
        parts = new_s.split('-')
        new_len, new_parts, i = 0, [], 0
        while len(new_parts) + len(parts[i]) + new_len <= 50:
            new_parts.append(parts[i])
            new_len += len(parts[i])
            i += 1
        new_s = '-'.join(new_parts)
    return new_s