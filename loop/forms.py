from django import forms
from django.utils.safestring import mark_safe
from loop.models import Broadcast, LoopUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from loop.configs import mergeentityconfig as merge_cnf

class BroadcastTestForm(forms.Form):
    to_number = forms.CharField(label='User Number', max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Enter a Phone Number'}))
    audio_file = forms.FileField(label='Select a WAV Audio file',
                               help_text='<span class="helptext" style="display:inline-block;">Upload .wav, 8Khz Mono format audio file with 16 bit depth(Max. Size 5MB)<br/> \
                               <a style="color:blue;" target="_blank" href="http://audio.online-convert.com/convert-to-wav">Click Here to Convert</a></span>'
                               )

    def __init__(self, *args, **kwargs):
        super(BroadcastTestForm, self).__init__(*args, **kwargs)
        self.fields['audio_file'].error_messages = {'required':'Audio file is required'}

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
    cluster = forms.MultipleChoiceField(required=False, label='Select Cluster',choices=[],widget=forms.SelectMultiple(attrs={'class': 'chosen-select','multiple':'multiple'}))
    farmer_file = forms.FileField(required=False, label='Select a .csv file', help_text=mark_safe('<a style="color:blue;" href="%s">Sample CSV</a> (Upload a CSV file if broadcast is not for full cluster)'%('/media/social_website/uploads/loop/broadcast/farmer/Sample_Contact_List.csv',)))
    audio_file = forms.FileField(label='Select a .WAV Audio file',
                               help_text='<span class="helptext" style="display:inline-block;">Upload .wav, 8Khz Mono format audio file with 16 bit depth(Max. Size 5MB)<br/> \
                               <a style="color:blue;" target="_blank" href="http://audio.online-convert.com/convert-to-wav">Click Here to Convert</a></span>'
                               )

    def __init__(self, *args, **kwargs):
        super(BroadcastForm, self).__init__(*args, **kwargs)
        self.fields['cluster'].choices = [(cluster['id'],'%s (%s)'%(cluster['name'],cluster['village__village_name'])) for cluster in LoopUser.objects.filter(role=2).values('id', 'name', 'village__village_name')]
        self.fields['title'].error_messages = {'required':'Broadcast Title is required'}
        self.fields['audio_file'].error_messages = {'required':'Audio file is required'}

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
        cluster = self.cleaned_data.get('cluster')
        if farmer_file and farmer_file.size/(1024*1024.0) > 5:
            raise forms.ValidationError("Please upload a CSV file less than 5 MB")
        if not cluster and not farmer_file:
            raise forms.ValidationError("Please select atleast one Cluster or .csv file")
        return farmer_file

class MergeEntityForm(forms.Form):

    choice_set = [('', '----------')]   
    for key in merge_cnf.models:
        choice_set.append((key, merge_cnf.models[key]['display_value']))
    model = forms.ChoiceField(required=True,widget= forms.Select, label='Select Model:', choices=choice_set)
    merge_file = forms.FileField(required=True, label='Select a .xlsx file:',)
    email = forms.EmailField(required=True, label='Enter email address to receive status of merge request:')


    def __init__(self, *args, **kwargs):
        super(MergeEntityForm, self).__init__(*args, **kwargs)
        self.fields['merge_file'].error_messages = {'required':'Merge file is required'}
        self.fields['model'].error_messages = {'required':'Select model name'}
        self.fields['email'].error_messages = {'required': 'Enter email address'}
        self.fields['merge_file'].help_text = ""

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
            return email
        except validate_email.ValidationError:
            raise forms.ValidationError("Enter a valid email address")

    def clean_merge_file(self):
        file = self.cleaned_data.get('merge_file')
        if file.name.endswith('.xlsx'):
            return file
        else:
            raise forms.ValidationError('Incorrect file type. Upload only .xlsx file')