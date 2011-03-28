"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.conf import settings
import re

def modify_redirect(request, redirect_to=None):
    if request.user.groups.filter(name=settings.STUDENT_GROUP_NAME).count() > 0:
        type = "student"
    elif request.user.groups.filter(name=settings.EMPLOYER_GROUP_NAME).count() > 0: 
        type = "employer"
    else:
        type = "student"
    if not redirect_to or ' ' in redirect_to or '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        if type == "employer":
            redirect_to = "/employer/%s/" % request.user
        else:
            redirect_to = "/student/%s/" % request.user
    return redirect_to