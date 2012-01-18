from django import template

register = template.Library()

@register.simple_tag
def selected_choice(form, field_name):
    return dict(form.fields[field_name].choices)[form.cleaned_data[field_name]]