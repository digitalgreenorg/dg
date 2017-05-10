from django import forms
from loop.models import Broadcast, LoopUser

class BroadcastTestForm(forms.Form):
    to_number = forms.CharField(label='User Number', max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Enter a Phone Number'}))
    audio_file = forms.FileField(label='Select a WAV Audio file',
                               help_text='Upload .wav, 8Khz Mono format audio file with 16 bit depth(Max. Size 5MB)'
                               )

    def clean_to_number(self):
        to_number = self.cleaned_data.get('to_number')
        if to_number == '' or len(to_number) < 10 or len(to_number) > 11:
            raise forms.ValidationError("Please Correct Phone Number.")
        if not all(digit.isdigit() for digit in to_number):
            raise forms.ValidationError("Number should contain only digits")
        if int(to_number) < 7000000000 or int(to_number) > 9999999999:
            raise forms.ValidationError("Please Correct Phone Number.")
        return to_number

    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file.content_type != 'audio/wav':
            raise forms.ValidationError("Please upload a WAV Audio file.")
        # .size returns size in bytes
        if audio_file.size/(1024*1024.0) > 5:
             raise forms.ValidationError("Please upload a WAV Audio file less than 5 MB")
        return audio_file


class BroadcastForm(forms.Form):
    title = forms.CharField(label='Broadcast Title',widget=forms.TextInput(attrs={'placeholder': 'Enter Meaningful Broadcast Title'}),max_length=Broadcast._meta.get_field('title').max_length)
    cluster = forms.ChoiceField(label='Select Cluster',choices=[])
    farmer_file = forms.FileField(required=False, label='Select a .csv file', help_text='Upload a CSV file with Farmers mobile number only if broadcast is not for full cluster')
    audio_file = forms.FileField(label='Select a .WAV Audio file',
                               help_text='Upload .WAV, 8Khz Mono format audio file with 16 bit depth(Max. Size 5MB)'
                               )

    def __init__(self, *args, **kwargs):
        super(BroadcastForm, self).__init__(*args, **kwargs)
        self.fields['cluster'].choices = [('','Select a Cluster')] + [(cluster['id'],'%s (%s)'%(cluster['name'],cluster['village__village_name'])) for cluster in LoopUser.objects.filter(role=2).values('id', 'name', 'village__village_name')]

    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file.content_type != 'audio/wav':
            raise forms.ValidationError("Please upload a WAV Audio file.")
        # .size returns size in bytes
        if audio_file.size/(1024*1024.0) > 5:
             raise forms.ValidationError("Please upload a WAV Audio file less than 5 MB")
        return audio_file

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == 'admin_test' or title.strip() == 'admin_test':
            raise forms.ValidationError("Please select another Meaningful name")
        return title

    def clean_farmer_file(self):
        farmer_file = self.cleaned_data.get('farmer_file')
        # if farmer_file.content_type != 'text/csv':
        #     raise forms.ValidationError("Please upload a CSV file only.")
        # .size returns size in bytes
        if farmer_file.size/(1024*1024.0) > 5:
             raise forms.ValidationError("Please upload a CSV file less than 5 MB")
        return farmer_file
