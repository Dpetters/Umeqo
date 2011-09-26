from django import forms
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode

from events.choices import TIME_CHOICES

class ImprovedSplitDateTimeWidget(forms.MultiWidget):
    """
    Copied from SplitDateTimeWidget, but also adds a class to date and time for js/css customization:
    A Widget that splits datetime input into two <input type="text"> boxes.
    """

    def __init__(self, attrs, dateAttrs={'class':'datefield'}, timeAttrs={'class':'timefield'}, date_format=None, time_format=None, initial=None):
        widgets = (forms.DateInput(attrs=dateAttrs, format="%m/%d/%Y"),
                   forms.Select(attrs=timeAttrs, choices=TIME_CHOICES))
        super(ImprovedSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            thedate = value.date()
            thetime = value.time().replace(minute=(value.minute/30)*30).strftime("%H:%M")
            return [thedate, thetime]
        return [None, None]
        
    class Media:
        css = {
            'all': ('css/datetime_field.css',),
        }

class UmSelectWidget(forms.Select):
    def render_option(self, selected_choices, option_value, option_label, extra=""):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        return u'<option value="%s"%s %s>%s</option>' % (
            escape(option_value), selected_html, extra,
            conditional_escape(force_unicode(option_label)))