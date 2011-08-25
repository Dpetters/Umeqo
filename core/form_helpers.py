from django.utils.html import escape

def boolean_coerce(value):
    # value is received as a unicode string
    if str(value).lower() in ( '1', 'true' ):
        return True
    elif str(value).lower() in ( '0', 'false' ):
        return False
    return None

def add_required_label_tag(original_function):
    """Adds the 'required' CSS class and an asterisks to required field labels."""
    def required_label_tag(self, contents=None, attrs=None):
        contents = contents or escape(self.label)
        if self.field.required:
            if not self.label.endswith("<span class='error'>*</span>"):
                self.label += "<span class='error'>*</span>"
                contents += "<span class='error'>*</span>"
            attrs = {'class': 'required'}
        return original_function(self, contents, attrs)
    return required_label_tag

def decorate_bound_field():
    from django.forms.forms import BoundField  
    BoundField.label_tag = add_required_label_tag(BoundField.label_tag)