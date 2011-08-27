from django.contrib.auth.models import User

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
