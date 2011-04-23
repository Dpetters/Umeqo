"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
import re
from django.core.urlresolvers import reverse

def modify_redirect(request, redirect_to=None):
    if not redirect_to or ' ' in redirect_to or '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        if hasattr(request.user, 'employer'):
            redirect_to = reverse('home')
        elif hasattr(request.user, "student"):
            redirect_to = reverse('home')
    return redirect_to