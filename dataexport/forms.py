from django import forms
from django.forms.extras.widgets import SelectDateWidget


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