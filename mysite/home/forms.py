from django import forms
from .models import Headline

class HeadlineForm(forms.ModelForm):
    class Meta:
        model = Headline
        fields = ['headline_name','headline_desc','headline_content','headline_image']

CHARACTERISTICS = (
    ('1', 'all'),
    ('2', 'age'), 
    ('3', 'race'),
    ('4', 'sex'), 
    ('5', 'sexual orientation'),
    ('6', 'gender identity'), 
    ('7', 'household income'),
    ('8', 'urban, suburban, or rural'),
    ('9', 'reported to police'), 
    ('10', 'did not report to police'),
)

CRIMES = (
    ('1', 'all violent victimizations'), 
    ('2', 'all property victimizations'),
    ('3', 'thefts and attempted thefts'),
    ('4', 'breakins and attempted breakins'), 
    ('5', 'motor vehicle thefts'),
    ('6', 'attacks and threats'), 
    ('7', 'unwanted sex'),
)

RATE_OR_NUMBER = (
    ('1', 'rate'),
    ('2', 'number'),
)

class SelectionForm(forms.Form):
    personal_characteristics = forms.ChoiceField(choices=CHARACTERISTICS)
    crime_type = forms.ChoiceField(choices=CRIMES)
    rate_or_number = forms.ChoiceField(choices=RATE_OR_NUMBER)