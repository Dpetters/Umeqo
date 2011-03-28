"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.dispatch import Signal


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])
