from dg.dashboard.models import *
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import *

class LanguageForm(ModelForm):
        class Meta:
                model = Language

class RegionForm(ModelForm):
        class Meta:
                model = Region

class RegionTestForm(ModelForm):
	class Meta:
		model = RegionTest

class StateForm(ModelForm):
	class Meta:
		model = State

class DistrictForm(ModelForm):
	class Meta:
		model = District


class BlockForm(ModelForm):
	class Meta:
		model = Block


class PersonGroupsForm(forms.ModelForm):
        #village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
        class Meta:
                model = PersonGroups

class PersonForm(forms.ModelForm):
	class Meta:
		model = Person	
		exclude=('equipmentholder','relations','adopted_agricultural_practices',)
		  
class DevelopmentManagerForm(forms.ModelForm):
	class Meta:
		model = DevelopmentManager

class FieldOfficerForm(forms.ModelForm):
	class Meta:
		model = FieldOfficer

class PartnerForm(forms.ModelForm):
	class Meta:
		model = Partners

class AnimatorForm(forms.ModelForm):
	class Meta:
		model = Animator
		exclude = ('assigned_villages',)

class AnimatorAssignedVillageForm(forms.ModelForm):
	class Meta:
		model = AnimatorAssignedVillage

class PracticeForm(forms.ModelForm):
	class Meta:
		model = Practices

class VillageForm(forms.ModelForm):
	class Meta:
		model = Village

class VideoForm(forms.ModelForm):
	class Meta:
		model = Video

class ScreeningForm(forms.ModelForm):
	class Meta:
		model = Screening
		exclude = ('farmers_attendance',)
