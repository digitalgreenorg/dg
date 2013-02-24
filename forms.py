from dashboard.models import *
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import *

# function for saving formsets with user information
def save_all(instances, user, id):
    for instance in instances:
        if(id):
            if instance.user_created_id == None:
                instance.user_created_id = user
            instance.user_modified_id = user
        else:
            instance.user_created_id = user
        instance.save()

class CocoModelForm(ModelForm):
    def save(self, commit=True, user = None, id = None,  *args, **kwargs):
        instance = super(CocoModelForm, self).save(commit=False)
        if (id):
            instance.user_modified_id = user
        else:
            instance.user_created_id = user
        if commit:
            instance.save()
            self.save_m2m()  
        return instance
        
    class Meta:
        model = CocoModel
        exclude = ('user_modified')

class LanguageForm(CocoModelForm):
    class Meta:
        model = Language

class CountryForm(CocoModelForm):
    class Meta:
        model = Country
        
class RegionForm(CocoModelForm):
    class Meta:
        model = Region

class RegionTestForm(CocoModelForm):
    class Meta:
        model = RegionTest

class StateForm(CocoModelForm):
    class Meta:
        model = State

class DistrictForm(CocoModelForm):
    class Meta:
        model = District

class BlockForm(CocoModelForm):
    class Meta:
        model = Block

class EquipmentForm(CocoModelForm):
    class Meta:
        model = Equipment

class PersonGroupsForm(CocoModelForm):
#    village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
    class Meta:
        model = PersonGroups
      
class PersonAdoptPracticeForm(CocoModelForm):
#    village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
    class Meta:
        model = PersonAdoptPractice
        exclude = ('practice',)

class PersonForm(CocoModelForm):
    class Meta:
        model = Person    
        exclude=('equipmentholder','relations','adopted_agricultural_practices',)
          
class DevelopmentManagerForm(CocoModelForm):
    class Meta:
        model = DevelopmentManager

class FieldOfficerForm(CocoModelForm):
    class Meta:
        model = FieldOfficer

class PartnerForm(CocoModelForm):
    class Meta:
        model = Partners

class AnimatorForm(CocoModelForm):
    class Meta:
        model = Animator
        exclude = ('assigned_villages',)

class AnimatorAssignedVillageForm(CocoModelForm):
    class Meta:
        model = AnimatorAssignedVillage

class PracticeForm(CocoModelForm):
    class Meta:
        model = Practices

class VillageForm(CocoModelForm):
    class Meta:
        model = Village

class VideoForm(CocoModelForm):       
    class Meta:
        model = Video
        exclude = ('related_practice',)

class PersonShownInVideoForm(CocoModelForm):
    class Meta:
        model = PersonShownInVideo

class ScreeningForm(CocoModelForm):
    class Meta:
        model = Screening
        exclude = ('farmers_attendance')

class GroupsTargetedInScreeningForm(CocoModelForm):
    class Meta:
        model = GroupsTargetedInScreening        
        
class VideosScreenedInScreeningForm(CocoModelForm):
    class Meta:
        model = VideosScreenedInScreening        
        
class TrainingForm(CocoModelForm):
    class Meta:
        model = Training
        
class TrainingAnimatorsTrainedForm(CocoModelForm):
    class Meta:
        model = TrainingAnimatorsTrained    

class MonthlyCostPerVillageForm(CocoModelForm):
    class Meta:
        model = MonthlyCostPerVillage
        
class PersonRelationsForm(CocoModelForm):
    class Meta:
        model = PersonRelations

class AnimatorSalaryPerMonthForm(CocoModelForm):
    class Meta:
        model = AnimatorSalaryPerMonth
        
class PersonMeetingAttendanceForm(CocoModelForm):
    class Meta:
        model = PersonMeetingAttendance
        
class EquipmentHolderForm(CocoModelForm):
    class Meta:
        model = EquipmentHolder
        
class ReviewerForm(CocoModelForm):
    class Meta:
        model = Reviewer

class TargetForm(CocoModelForm):
    class Meta:
        model = Target
