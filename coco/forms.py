from django import forms
from .validators import validate_file_extension


def validate_file_extension(value):
    if not value.name.endswith('.json'):
        raise forms.ValidationError(u'Please upload a Json File')



class DataUploadForm(forms.Form):
	datafile = forms.FileField(label='Select a file',
                               help_text='max 4MB',
                               required=True,
                               validators=[validate_file_extension])

	def clean_data_file(self):
		cd = self.cleaned_data
		if cd.get('datafile').name != "export-data.json":
			raise forms.ValidationError("Please upload correct File")
		return self.cleaned_data.get('datafile')

	


