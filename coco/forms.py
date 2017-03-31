from django import forms
from .validators import validate_file_extension

class DataUploadForm(forms.Form):
	datafile = forms.FileField(label='Select a file',
                               help_text='max 4MB',
                               required=True,
                               validators=[validate_file_extension])

	


