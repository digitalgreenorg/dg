from django import forms
from loop.models import Broadcast, BroadcastUser

class BroadcastTestForm(forms.Form):
	to_number = forms.CharField(max_length=20, required=True)
	audio_file = forms.FileField(label='Select a WAV Audio file',
                               help_text='Max 5MB',
                               required=True,
                               )

	def clean_to_number(self):
		to_number = self.cleaned_data.get('to_number')
		if to_number == '' or len(to_number) < 10 or len(to_number) > 11 or to_number < '7000000000' or to_number > '9999999999':
			raise forms.ValidationError("Please Correct Phone Number.")
		if not all(digit.isdigit() for digit in to_number):
			raise forms.ValidationError("Number should contain only digits")
		return to_number

	def clean_audio_file(self):
		print "In clean audio"
		audio_file = self.cleaned_data.get('audio_file')
		if audio_file.content_type != 'audio/wav':
			raise forms.ValidationError("Please upload a WAV Audio file.")
		# .size return size in bytes
		if audio_file.size/(1024*1024.0) > 5:
			 raise forms.ValidationError("Please upload a WAV Audio file less than 5 MB")
		return audio_file
