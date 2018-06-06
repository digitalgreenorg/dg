from django import forms
from geographies.models import Country
from geographies.models import State



DATA_CATEGORY = [
    ('3', 'All'),
    ('1', 'Health & Nutrition'),
    ('2', 'Agriculture'),
    
]

DATA = [
    ('1', 'Screening'),
    ('2', 'Adoption'),
]


class PageView(forms.Form):
    date_period = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    # end_date = forms.DateField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    data_category = forms.ChoiceField(choices=DATA_CATEGORY, required=True, widget=forms.Select(attrs={'class' : 'form-control'}))
    data = forms.ChoiceField(choices=DATA, required=True, widget=forms.Select(attrs={'class' : 'form-control'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=True,\
                                     empty_label=None,widget=forms.Select(attrs={'class' : 'form-control'}),
                                     to_field_name="id")
    state = forms.CharField(
                                   widget=forms.Select(attrs={'class' : 'form-control', 'multiple': 'multiple'}),
                                   required=False,
                                   )