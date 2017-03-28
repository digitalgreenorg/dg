from django import forms

class DataUploadForm(forms.Form):
	datafile = forms.FileField(label='Select a file',
                               help_text='max 2MB',
                               required=True)

