import operator
from django import forms
from django.conf import settings
from django.conf.urls import patterns
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import smart_str
from django.forms import TextInput, Textarea
from coco.base_models import NONNEGOTIABLE_OPTION
from activities.models import PersonMeetingAttendance, Screening, PersonAdoptPractice, FrontLineWorkerPresent
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from dashboard.forms import CocoUserForm
from qacoco.forms import QACocoUserForm
from qacoco.admin import QACocoUserAdmin
from videos.models import  NonNegotiable
from videos.models import *
from programs.models import Project
from easy_select2 import Select2Multiple, Select2


class PersonMeetingAttendanceForm(forms.ModelForm):
    person = forms.ModelChoiceField(Animator.objects.none())
    class Meta:
        model = PersonMeetingAttendance
        exclude = ()

class FarmerAttendanceInline(admin.TabularInline):
    model = PersonMeetingAttendance
    raw_id_fields = ("person",)
    extra = 20


class ScreeningForm(forms.ModelForm):
    class DynamicChoiceField(forms.ChoiceField):
        def clean(self, value):
            return value

    class DynamicMultipleChoiceField(forms.MultipleChoiceField):
        def clean(self, value):
            return value


    #village  = AjaxForeignKeyField(Village, (('village_name',{}),),default_index=0, select_related= None, widget=FilteredSelect(attrs={'onchange':'temp();'}))
    #village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'filter();'}))
    #animator = DynamicChoiceField(widget=forms.Select(attrs={'disabled': 'true'}))
    farmer_groups_targeted = forms.ModelMultipleChoiceField(PersonGroup.objects, widget=forms.SelectMultiple(attrs={'onchange': 'filter_person();'}))
    #farmer_groups_targeted = DynamicMultipleChoiceField(widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))
    #farmer_groups_targeted = forms.ModelMultipleChoiceField(queryset=PersonGroup.objects.none())
    #animator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))
    animator = forms.ModelChoiceField(Animator.objects)
    #screening_grade = forms.ChoiceField(widget=forms.RadioSelect(), choices=SCREENING_GRADE)
    #farmers_groups_targeted = forms.ModelChoiceField(PersonGroup.objects, widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))

    class Meta:
        model = Screening
        exclude = ()

class ScreeningAdmin(admin.ModelAdmin):
    filter_horizontal = ('videoes_screened',)
    list_display = ('id', 'date', 'screening_location', 'observation_status', 'screening_grade', 'observer')
    search_fields = ['user_created__username', 'id', 'village__village_name', 'partner__partner_name','animator__name', 'videoes_screened__title', 'village__block__block_name', 'village__block__district__district_name','village__block__district__state__state_name']
    raw_id_fields = ('village', 'animator', 'farmer_groups_targeted', 'videoes_screened')
    list_filter = ('date', 'observation_status', 'screening_grade', 'village__block__district__state__state_name',  'partner__partner_name', 'observer')
    list_editable = ('observation_status', 'screening_grade', 'observer')
    class Media:
        js = (
                settings.STATIC_URL + "js/qa_screening.js",
        )

class NonNegotiablesInline(admin.TabularInline):
    model =  NonNegotiable
    raw_id_fields = ("video",)
    extra = 10


class ParentCategoryAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    list_display = ['id', 'parent_category_name']
    search_fields = ['parent_category_name']


class FrontLineWorkerPresentAdmin(admin.ModelAdmin):
    

    list_display = ['id', 'worker_type']
    search_fields = ['worker_type']


class DirectBeneficiariesAdmin(admin.ModelAdmin):

    list_display = ['id', 'direct_beneficiaries_category']
    search_fields = ['direct_beneficiaries_category']



class VideoAdmin(admin.ModelAdmin):
    inlines = [NonNegotiablesInline]
    fieldsets = [
                (None, {'fields':['title','video_type','production_date','language','benefit', 'partner', 'related_practice', 'category','subcategory','videopractice']}),
                (None,{'fields':['village','production_team']}),
                ('Review', {'fields': ['approval_date','youtubeid','review_status','video_grade','reviewer']}),
    ]
    list_display = ('id', 'title', 'category',  'location', 'production_date', 'review_status', 'video_grade', 'reviewer')
    search_fields = ['id', 'title', 'category__category_name', 'partner__partner_name' , 'village__village_name', 'village__block__block_name', 'village__block__district__district_name','village__block__district__state__state_name' ]
    list_filter = ('review_status', 'category', 'video_grade', 'village__block__district__state__state_name', 'partner__partner_name', 'reviewer')
    list_editable = ('review_status', 'video_grade', 'reviewer')
    raw_id_fields = ('village', 'production_team', 'related_practice')
    class Media:
        js = (
                settings.STATIC_URL + "js/qa_video.js",
        )

class AnimatorAssignedVillages(admin.StackedInline):
    model = AnimatorAssignedVillage


class AnimatorAdmin(admin.ModelAdmin):
    fields = ('name','gender','phone_no','partner','district','role')
    inlines = [AnimatorAssignedVillages]
    list_display = ('name', 'partner', 'district', 'role',)
    search_fields = ['name', 'partner__partner_name', 'role',]
    

class PersonGroupInline(admin.TabularInline):
    model = PersonGroup
    extra = 5

class AnimatorInline(admin.TabularInline):
    model = Animator
    extra = 5
    exclude = ('assigned_villages',)

class VillageAdmin(admin.ModelAdmin):
    list_display = ('village_name', 'block')
    search_fields = ['village_name', 'block__block_name', 'block__district__state__state_name']
    inlines = [PersonGroupInline]


class PersonInline(admin.TabularInline):
    model = Person
    extra = 30


class PersonGroupForm(forms.ModelForm):
    class Meta:
        model = PersonGroup
        exclude = ()

    class Media:
        js = (
                settings.STATIC_URL + "js/filter_village.js",
                #settings.STATIC_URL + "js/jquery-1.3.2.min.js",
                #settings.STATIC_URL + "js/ui/ui.core.js",
                #settings.STATIC_URL + "js/ui/ui.sortable.js",
                #settings.STATIC_URL + "js/dynamic_inlines_with_sort.js",
        )

        #css = {
        #        'all':('/media/css/dynamic_inlines_with_sort.css',)
        #}



class PersonGroupAdmin(admin.ModelAdmin):
    inlines = [PersonInline]
    list_display = ('group_name','village')
    search_fields = ['group_name','village__village_name']
    form = PersonGroupForm


class AnimatorAssignedVillageAdmin(admin.ModelAdmin):
    list_display = ('animator','village')
    search_fields = ['animator__name','village__village_name']


class PersonAdoptPracticeInline(admin.StackedInline):
    model = PersonAdoptPractice
    extra = 3

class PersonAdoptPracticeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.CheckboxSelectMultiple(choices=NONNEGOTIABLE_OPTION)},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    list_display = ('id', 'date_of_adoption', '__unicode__', 'verification_status', 'non_negotiable_check', 'verified_by')
    list_editable = ('verification_status','non_negotiable_check', 'verified_by')
    list_filter = ('date_of_adoption', 'verification_status','person__village__block__district__state__state_name', 'person__village__block__district__district_name','person__village__block__block_name','person__village__block__village__village_name','partner__partner_name', 'verified_by')
    search_fields = ['user_created__username', 'id', 'person__person_name', 'person__father_name',
                     'person__village__block__block_name', 'video__title',
                     'person__group__group_name','person__village__block__block_name',
                     'person__village__block__district__district_name',
                     'person__village__block__district__state__state_name',
                     'date_of_adoption',
                     'date_of_verification']
    raw_id_fields = ('person', 'video')

    class Media:
        js = (
                settings.STATIC_URL + "js/qa_verification.js",
        )


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__' , 'age', 'gender' ,'partner', 'is_modelfarmer')
    search_fields = ['person_name','village__village_name','group__group_name']
    raw_id_fields = ('village','group')

class BlockAdmin(admin.ModelAdmin):
    list_display = ('block_name', 'district')
    search_fields = ['block_name', 'district__district_name', 'district__state__state_name']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'state')
    search_fields = ['district_name', 'state__state_name']

class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name',)
    search_fields = ['state_name', 'country__country_name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category')
    search_fields = ['subcategory_name', 'category__category_name']

class VideoPracticeAdmin(admin.ModelAdmin):
    list_display = ('videopractice_name', 'subcategory')
    search_fields = ['videopractice_name', 'subcategory__subcategory_name']

class PracticesAdmin(admin.ModelAdmin):
    list_display = ('id', 'practice_name', 'practice_sector', 'practice_subject', 'practice_subsector', 'practice_topic', 'practice_subtopic')
    search_fields = ['id', 'practice_name', 'practice_sector__name', 'practice_subject__name', 'practice_subsector__name', 'practice_topic__name', 'practice_subtopic__name']

class PracticeSectorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PracticeSubSectorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PracticeTopicAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PracticeSubtopicAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PracticeSubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']

class CocoUserAdmin(admin.ModelAdmin):
    form = CocoUserForm
    list_display = ('user','partner','get_villages')
    search_fields = ['user__username']

class QACocoUserAdmin(admin.ModelAdmin):
    form = QACocoUserForm
    list_display = ('user','partner','get_blocks')
    search_fields = ['user__username']

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('associate_partner',)
    list_display = ('id','project_name')
    search_fields = ['project_name']


class VideoForm(forms.ModelForm):
    video = forms.ModelChoiceField(queryset=None, widget=Select2(select2attrs={'width': '600px'}),required=True)
    bluefrog_practice = forms.ModelMultipleChoiceField(queryset=BluefrogPractice.objects.all(), widget=Select2Multiple(select2attrs={'width': '600px'}),required=True)
    bluefrog_subcategory = forms.ModelChoiceField(queryset=BluefrogSubcategory.objects.all(), widget=Select2(select2attrs={'width': '600px'}),required=True)
    districtscreening = forms.ModelMultipleChoiceField(queryset=DistrictScreening.objects.all(), widget=Select2Multiple(select2attrs={'width': '600px'}),required=True)

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['video'].queryset = Video.objects.filter(partner_id=50)



class BluefrogSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['crop_id', 'crop_name', 'crop_name_telgu']
    search_fields = ['crop_id', 'crop_name', 'crop_name_telgu']


class BluefrogPracticeAdmin(admin.ModelAdmin):
    list_display = ['practice_id', 'practice_method_name', 'practice_method_name_telgu']
    search_fields = ['practice_id', 'practice_method_name', 'practice_method_name_telgu']


class DistrictScreeningAdmin(admin.ModelAdmin):
    list_display = ['id', 'districtscreening_id', 'districtscreening_name']


class APVideoAdmin(admin.ModelAdmin):

    form = VideoForm
    list_display = ['id', 'short_video_title', 'video_short_name', 'video_short_regionalname', 'bluefrog_practice']
    search_fields = ['id', 'video', 'video_short_name', 'video_short_regionalname', 'bluefrog_practice']
    # list_editable = ['video_short_name', 'video_short_regionalname', 'bluefrog_practice']


