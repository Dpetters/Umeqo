from django import forms

from core import messages as m
from student.decorators import is_student

def verify_account(user):
    if not user.userattributes.is_verified and not user.is_active:
        raise forms.ValidationError(m.account_suspended)
    # We only care about verified if the user is a student
    if is_student(user) and not user.userattributes.is_verified and user.is_active:
        raise forms.ValidationError(m.not_activated)