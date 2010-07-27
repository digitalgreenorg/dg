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

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment

class PersonGroupsForm(forms.ModelForm):
        #village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
        class Meta:
                model = PersonGroups
class PersonAdoptPracticeForm(forms.ModelForm):
        #village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
        class Meta:
                model = PersonAdoptPractice

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

class VideoAgriculturalPracticesForm(forms.ModelForm):       
    class Meta:
        model = VideoAgriculturalPractices

class PersonShownInVideoForm(forms.ModelForm):
    class Meta:
        model = PersonShownInVideo

class ScreeningForm(forms.ModelForm):
	class Meta:
		model = Screening
		exclude = ('farmers_attendance',)

class GroupsTargetedInScreeningForm(forms.ModelForm):
    class Meta:
        model = GroupsTargetedInScreening        
        
class VideosScreenedInScreeningForm(forms.ModelForm):
    class Meta:
        model = VideosScreenedInScreening        
		
class TrainingForm(forms.ModelForm):
	class Meta:
		model = Training
        
class TrainingAnimatorsTrainedForm(forms.ModelForm):
    class Meta:
        model = TrainingAnimatorsTrained    

class MonthlyCostPerVillageForm(forms.ModelForm):
	class Meta:
		model = MonthlyCostPerVillage
		
class PersonRelationsForm(forms.ModelForm):
	class Meta:
		model = PersonRelations

class AnimatorSalaryPerMonthForm(forms.ModelForm):
	class Meta:
		model = AnimatorSalaryPerMonth
		
class PersonMeetingAttendanceForm(forms.ModelForm):
    class Meta:
        model = PersonMeetingAttendance
		
class EquipmentHolderForm(forms.ModelForm):
	class Meta:
		model = EquipmentHolder
		
class ReviewerForm(forms.ModelForm):
	class Meta:
		model = Reviewer

class TargetForm(forms.ModelForm):
    class Meta:
        model = Target