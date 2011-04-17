"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
import re

def modify_redirect(request, redirect_to=None):
    if not redirect_to or ' ' in redirect_to or '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        if hasattr(request, "employer"):
            redirect_to = "/employer/%s/" % request.user
        elif hasattr(request, "student"):
            redirect_to = "/student/%s/" % request.user
    return redirect_to