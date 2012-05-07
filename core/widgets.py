from django import forms
from django.forms.util import flatatt
from django.forms.widgets import RadioFieldRenderer, RadioInput
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
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

class UmRadioInput(RadioInput):

    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = force_unicode(choice[0])
        self.choice_label = force_unicode(choice[1])
        self.extra_attribute = force_unicode(choice[2])
        self.index = index
        
    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input%s %s/>' % (flatatt(final_attrs), self.extra_attribute))

    
class UmRadioFieldRenderer(RadioFieldRenderer):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield UmRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return UmRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)
                
                
class UmRadioSelect(forms.RadioSelect):
    renderer = UmRadioFieldRenderer
    """
    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label, extra in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label, extra))
        return u'\n'.join(output)
    """