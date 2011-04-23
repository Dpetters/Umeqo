"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
import re

def modify_redirect(request, redirect_to=None):
    if not redirect_to or ' ' in redirect_to or '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        if hasattr(request.user, 'employer'):
            redirect_to = "/employer/"
        elif hasattr(request.user, "student"):
            redirect_to = "/student/"
    print redirect_to
    return redirect_to