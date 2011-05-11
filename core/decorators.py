"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

def is_student(user):
    return hasattr(user, "student")
    
def is_employer(user):
    return hasattr(user, "employer")
