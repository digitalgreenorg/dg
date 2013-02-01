from dashboard.models import *
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import *

# function for saving formsets with user information
def save_all(instances, user, id):
    for instance in instances:
        if(id):
            instance.user_modified_id = user
        else:
            instance.user_created_id = user
        instance.save()

class UserInfoForm(ModelForm):
    def save(self, commit=True, user = None, id = None,  *args, **kwargs):
        instance = super(UserInfoForm, self).save(commit=False)
        if (id):
            instance.user_modified_id = user
        else:
            instance.user_created_id = user
        if commit:
            instance.save()
        return instance
        
    class Meta:
        model = UserInfo
        exclude = ('time_created','user_modified','time_modified')

class LanguageForm(UserInfoForm):
    class Meta:
        model = Language

class CountryForm(UserInfoForm):
    class Meta:
        model = Country
        
class RegionForm(UserInfoForm):
    class Meta:
        model = Region

class RegionTestForm(UserInfoForm):
    class Meta:
        model = RegionTest

class StateForm(UserInfoForm):
    class Meta:
        model = State

class DistrictForm(UserInfoForm):
    class Meta:
        model = District

class BlockForm(UserInfoForm):
    class Meta:
        model = Block

class EquipmentForm(UserInfoForm):
    class Meta:
        model = Equipment

class PersonGroupsForm(UserInfoForm):
    #village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
    class Meta:
        model = PersonGroups
      
class PersonAdoptPracticeForm(UserInfoForm):
    #village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
    class Meta:
        model = PersonAdoptPractice
        exclude = ('practice',)

class PersonForm(UserInfoForm):
    class Meta:
        model = Person    
        exclude=('equipmentholder','relations','adopted_agricultural_practices',)
          
class DevelopmentManagerForm(UserInfoForm):
    class Meta:
        model = DevelopmentManager

class FieldOfficerForm(UserInfoForm):
    class Meta:
        model = FieldOfficer

class PartnerForm(UserInfoForm):
    class Meta:
        model = Partners

class AnimatorForm(UserInfoForm):
    class Meta:
        model = Animator
        exclude = ('assigned_villages',)

class AnimatorAssignedVillageForm(UserInfoForm):
    class Meta:
        model = AnimatorAssignedVillage

class PracticeForm(UserInfoForm):
    class Meta:
        model = Practices

class VillageForm(UserInfoForm):
    class Meta:
        model = Village

class VideoForm(UserInfoForm):       
    class Meta:
        model = Video
        exclude = ('related_practice',)

class PersonShownInVideoForm(UserInfoForm):
    class Meta:
        model = PersonShownInVideo

class ScreeningForm(UserInfoForm):
    class Meta:
        model = Screening
        exclude = ('farmers_attendance',)

class GroupsTargetedInScreeningForm(UserInfoForm):
    class Meta:
        model = GroupsTargetedInScreening        
        
class VideosScreenedInScreeningForm(UserInfoForm):
    class Meta:
        model = VideosScreenedInScreening        
        
class TrainingForm(UserInfoForm):
    class Meta:
        model = Training
        
class TrainingAnimatorsTrainedForm(UserInfoForm):
    class Meta:
        model = TrainingAnimatorsTrained    

class MonthlyCostPerVillageForm(UserInfoForm):
    class Meta:
        model = MonthlyCostPerVillage
        
class PersonRelationsForm(UserInfoForm):
    class Meta:
        model = PersonRelations

class AnimatorSalaryPerMonthForm(UserInfoForm):
    class Meta:
        model = AnimatorSalaryPerMonth
        
class PersonMeetingAttendanceForm(UserInfoForm):
    class Meta:
        model = PersonMeetingAttendance
        
class EquipmentHolderForm(UserInfoForm):
    class Meta:
        model = EquipmentHolder
        
class ReviewerForm(UserInfoForm):
    class Meta:
        model = Reviewer

class TargetForm(UserInfoForm):
    class Meta:
        model = Target
