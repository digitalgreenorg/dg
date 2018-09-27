from django import forms
from geographies.models import *
from easy_select2 import Select2


class DataUploadForm(forms.Form):
	datafile = forms.FileField(label='Select a file',
                               help_text='max 4MB',
                               required=True,
                               )


class GeographyMappingForm(forms.Form):
    choices = (('District','District'),
                ('Block', 'Block'),
                ('Village','Village'))

    geographytype = forms.ChoiceField(choices=choices,widget=forms.Select(attrs={'class' : 'form-control', 'width':'300px'}))
    apgeo = forms.CharField(required=True,widget=forms.Select(attrs={'class' : 'form-control', 'width':'300px'}))
    cocogeo = forms.CharField(required=True, widget=forms.Select(attrs={'class' : 'form-control', 'width':'300px'}))


	


