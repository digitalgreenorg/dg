from django import forms


DATA_TABLE_CHOICES = (
    ('village', ("Village")),
    ('mediators', ("Mediators")),
    ('videos', ("Videos")),
    ('groups', ("Groups")),
    ('persons', ("Persons")),
    ('screening', ("Screening")),
    ('adoptions', ("Adoptions")),
)

class DataUploadForm(forms.Form):
	csvfile = forms.FileField(
        label='Select a file',
        help_text='max 2MB',
        required=True
    )