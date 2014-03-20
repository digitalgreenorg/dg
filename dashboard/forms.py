from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import *
from activities.models import PersonAdoptPractice, PersonMeetingAttendance, Screening
from geographies.models import Village, Block, Region, District, State, Country
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from programs.models import Partner
from videos.models import Language, Practice, Video

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

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s) (%s)" % (obj.village_name, obj.block.block_name, obj.block.district.district_name)


class CocoUserForm(forms.ModelForm):
    villages = UserModelMultipleChoiceField(
        widget=FilteredSelectMultiple(
                                      verbose_name='villages',
                                      is_stacked=False
                                     ),
        queryset=Village.objects.all()
        )


class LanguageForm(CocoModelForm):
    class Meta:
        model = Language

class CountryForm(CocoModelForm):
    class Meta:
        model = Country
        
class RegionForm(CocoModelForm):
    class Meta:
        model = Region

class StateForm(CocoModelForm):
    class Meta:
        model = State

class DistrictForm(CocoModelForm):
    class Meta:
        model = District

class BlockForm(CocoModelForm):
    class Meta:
        model = Block

class PersonGroupForm(CocoModelForm):
#    village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
    class Meta:
        model = PersonGroup
      
class PersonAdoptPracticeForm(CocoModelForm):
#    village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter_village();'}))
    class Meta:
        model = PersonAdoptPractice
        exclude = ('practice',)

class PersonForm(CocoModelForm):
    class Meta:
        model = Person    
        exclude=('equipmentholder','relations','adopted_agricultural_practices',)

class PartnerForm(CocoModelForm):
    class Meta:
        model = Partner

class AnimatorForm(CocoModelForm):
    class Meta:
        model = Animator
        exclude = ('assigned_villages',)
        
class AnimatorAssignedVillageForm(CocoModelForm):
    class Meta:
        model = AnimatorAssignedVillage

class PracticeForm(CocoModelForm):
    class Meta:
        model = Practice

class VillageForm(CocoModelForm):
    class Meta:
        model = Village

class VideoForm(CocoModelForm):       
    class Meta:
        model = Video
        exclude = ('related_practice',)

class ScreeningForm(CocoModelForm):
    class Meta:
        model = Screening
        exclude = ('farmers_attendance')   

class PersonMeetingAttendanceForm(CocoModelForm):
    class Meta:
        model = PersonMeetingAttendance
