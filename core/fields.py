import os

from core import messages as m

from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import FileInput
from django import forms

class PdfField(forms.Field):

    default_error_messages = {
        'invalid': _(m.invalid_file),
        'missing': _(m.missing_file),
        'empty': _(m.empty_file),
        'max_length': _(m.max_length),
        'invalid_type': _(m.invalid_type),
    }

    def __init__(self, *args, **kwargs):
        self.widget = FileInput
        self.max_length = kwargs.pop('max_length', None)
        super(PdfField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        if data in validators.EMPTY_VALUES:
            return None

        # UploadedFile objects should have name and size attributes.
        try:
            file_name = data.name
            file_size = data.size
        except AttributeError:
            raise ValidationError(self.error_messages['invalid'])
        
        ext = os.path.splitext(file_name)[1]
        ext = ext.lower()
        if ext != ".pdf":
            raise ValidationError(self.error_messages['invalid_type'])
        if self.max_length is not None and len(file_name) > self.max_length:
            error_values =  {'max': self.max_length, 'length': len(file_name)}
            raise ValidationError(self.error_messages['max_length'] % error_values)
        if not file_name:
            raise ValidationError(self.error_messages['invalid'])
        if not file_size:
            raise ValidationError(self.error_messages['empty'])

        return data

    def clean(self, data, initial=None):
        if not data and initial:
            return initial
        return super(PdfField, self).clean(data)