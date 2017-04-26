from django import forms
from loop.models import Broadcast, BroadcastUser, LoopUser

class BroadcastTestForm(forms.Form):
	to_number = forms.CharField(max_length=20)
	audio_file = forms.FileField(label='Select a WAV Audio file',
                               help_text='Upload .wav, 8Khz Mono format audio file with bit depth must be 16 bit (Max. Size 5MB)'
                               )

	def clean_to_number(self):
		to_number = self.cleaned_data.get('to_number')
		if to_number == '' or len(to_number) < 10 or len(to_number) > 11 or to_number < '7000000000' or to_number > '9999999999':
			raise forms.ValidationError("Please Correct Phone Number.")
		if not all(digit.isdigit() for digit in to_number):
			raise forms.ValidationError("Number should contain only digits")
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
	title = forms.CharField(label='Broadcast Title',widget=forms.TextInput(attrs={'placeholder': 'Broadcast Title'}),max_length=Broadcast._meta.get_field('title').max_length)
	cluster_choice = [('','Select a Cluster')] + [(cluster['id'],'%s (%s)'%(cluster['name'],cluster['village__village_name'])) for cluster in LoopUser.objects.filter(role=2).values('id', 'name', 'village__village_name')]
	cluster = forms.ChoiceField(label='Select Cluster',choices=cluster_choice)
	audio_file = forms.FileField(label='Select a .WAV Audio file',
                               help_text='Upload .WAV, 8Khz Mono format audio file with bit depth must be 16 bit (Max. Size 5MB)'
                               )

	def clean_audio_file(self):
		audio_file = self.cleaned_data.get('audio_file')
		if audio_file.content_type != 'audio/wav':
			raise forms.ValidationError("Please upload a WAV Audio file.")
		# .size returns size in bytes
		if audio_file.size/(1024*1024.0) > 5:
			 raise forms.ValidationError("Please upload a WAV Audio file less than 5 MB")
		return audio_file
