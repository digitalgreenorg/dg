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
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup, Household
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


class TagAdmin(admin.ModelAdmin):
    list_display = ['id','tag_name','is_ap_tag']
    search_fields = ['tag_name']


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

class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'partner_name']


class VideoAdmin(admin.ModelAdmin):
    inlines = [NonNegotiablesInline]
    fieldsets = [
                (None, {'fields':['title','video_type','production_date','language','benefit', 'partner', 'category','subcategory','videopractice', 'tags']}),
                (None,{'fields':['village','production_team']}),
                ('Review', {'fields': ['approval_date','youtubeid','review_status','video_grade','reviewer']}),
    ]
    list_display = ('id', 'title', 'category',  'location', 'production_date', 'review_status', 'video_grade', 'reviewer')
    search_fields = ['id', 'title', 'category__category_name', 'partner__partner_name' , 'village__village_name', 'village__block__block_name', 'village__block__district__district_name','village__block__district__state__state_name' ]
    list_filter = ('review_status', 'category', 'video_grade', 'village__block__district__state__state_name', 'partner__partner_name', 'reviewer')
    list_editable = ('review_status', 'video_grade', 'reviewer')
    raw_id_fields = ('village', 'production_team', 'related_practice')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Tag.objects.filter(is_ap_tag=False)
        return super(VideoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

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
    list_display = ('id', 'village_name', 'block', 'active')
    search_fields = ['village_name', 'block__block_name', 'block__district__state__state_name']
    inlines = [PersonGroupInline]


class PersonInline(admin.TabularInline):
    model = Person
    extra = 0

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

# class HouseholdForm(forms.ModelForm):
#     class Meta:
#         model = Household
#         fields = ("__all__")

    # class Media:
    #     js = (settings.STATIC_URL + "js/filter_village.js",)


class PersonGroupAdmin(admin.ModelAdmin):
    inlines = [PersonInline]
    list_display = ('group_name', 'village')
    search_fields = ['group_name', 'village__village_name']
    form = PersonGroupForm

class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('household_name', 'head_gender', 'village')
    list_filter = ('head_gender','village')
    search_fields = ['household_name']
    # form = HouseholdForm


class AnimatorAssignedVillageAdmin(admin.ModelAdmin):
    list_display = ('animator','village')
    search_fields = ['animator__name', 'village__village_name']


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
    list_display = ('id', 'block_name', 'district', 'active')
    search_fields = ['block_name', 'district__district_name', 'district__state__state_name']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'district_name', 'state', 'active')
    search_fields = ['district_name', 'state__state_name']

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'state_name','active')
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
    list_display = ('id', 'user', 'partner','get_villages')
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
    practice = forms.ModelMultipleChoiceField(queryset=APPractice.objects.all(), widget=Select2Multiple(select2attrs={'width': '600px'}),required=True)
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), widget=Select2(select2attrs={'width': '600px'}),required=True)
    aptags = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(is_ap_tag=True), widget=Select2Multiple(select2attrs={'width': '600px'}),required=True)

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        mapped_videos = list(APVideo.objects.values_list('video_id',flat=True).distinct())
        if kwargs.get('instance'):
            instance_video_id = kwargs.get('instance').video_id
            mapped_videos.remove(instance_video_id)        
        self.fields['video'].queryset = Video.objects.filter(partner_id__in=(50,72),village__block__district__state_id= 6).exclude(id__in=mapped_videos)


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
    list_display = ['id', 'short_video_title', 'video_short_name',
                    'video_short_regionalname']
    search_fields = ['id', 'video', 'video_short_name',
                     'video_short_regionalname', 'practice']
    def save_related(self, request, form, formsets, change):
        super(APVideoAdmin, self).save_related(request, form, formsets, change)
        current_instance_tag = form.cleaned_data.get('aptags')
        tag_id_to_be_removed = form.instance.video.tags.values_list('id', flat=True)
        if tag_id_to_be_removed:
            form.instance.video.tags.remove(*tag_id_to_be_removed)
        form.instance.video.tags.add(*current_instance_tag)


class AP_DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'district_code', 'district_name', 'user_created',
                    'time_created', '_district']
    search_fields = ['id', 'district_code', 'district_name', 'district__id']

    def _district(self, obj):
        return "%s:%s" % (obj.district.id, obj.district.district_name)
    _district.allow_tags = True
    _district.short_description = "COCO-DB-District-ID"


class AP_BlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'mandal_code', 'mandal_name',
                    'user_created', 'time_created', '_block']
    search_fields = ['id', 'mandal_code', 'mandal_name', 'block', 'district_code']

    def _block(self, obj):
        return "%s:%s" % (obj.block.id, obj.block.block_name)
    _block.allow_tags = True
    _block.short_description = "COCO-DB-Block-ID"


class AP_VillageAdmin(admin.ModelAdmin):
    list_display = ['id', 'village_code', 'village_name', 'ap_mandal',
                    'user_created', 'time_created', '_village']
    search_fields = ['id', 'village_code', 'village_name', 'village__id']
    readonly_fields = list_display

    def _village(self, obj):
        return "%s:%s" % (obj.village.id, obj.village.village_name)
    _village.allow_tags = True
    _village.short_description = "COCO-DB-Village-ID"

    def has_add_permission(self, request):
        return False


class AP_COCO_MappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'geo_type', 'ap_geo_id', 'coco_geo_id', 'user_created_id', 'user_modified_id', 'time_created','time_modified']
    search_fields = ['id', 'geo_type', 'ap_geo_id', 'coco_geo_id']
    list_filter = ['geo_type']


class AP_HabitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'habitation_code', 'habitation_name', 'ap_village',
                    'user_created', 'time_created']
    search_fields = ['id', 'habitation_code', 'habitation_name', 'ap_village__village_code', 'ap_village__id']
    readonly_fields = list_display

    def has_add_permission(self, request):
        return False


class APCropAdmin(admin.ModelAdmin):
    list_display = ['id', 'crop_code', 'crop_name', 'crop_name_telgu', 'user_created',
                    'time_created', '_subcategory']
    search_fields = ['id', 'crop_code', 'crop_name']

    def _subcategory(self, obj):
        return "%s:%s" % (obj.subcategory.id, obj.subcategory.subcategory_name)
    _subcategory.allow_tags = True
    _subcategory.short_description = "COCO-DB-Person-ID"


class APPracticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'pest_code', 'pest_name', 'pest_name_telgu', 'user_created',
                    'time_created']
    search_fields = ['id', 'pest_code', 'pest_name']


class AP_PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_code', 'person', 'user_created',
                    'time_created', '_person']
    search_fields = ['id', 'person_code', 'person__id']

    def _person(self, obj):
        return "%s:%s" % (obj.person.id, obj.person.person_name)
    _person.allow_tags = True
    _person.short_description = "COCO-DB-Person-ID"


class AP_AnimatorAdmin(admin.ModelAdmin):
    list_display = ['id','animator_code', 'designation',  'user_created', 'time_created',
                    '_animator']
    search_fields = ['id', 'animator_code', 'designation']

    def _animator(self, obj):
        return "%s:%s" % (obj.animator.id, obj.animator.name)
    _animator.allow_tags = True
    _animator.short_description = "COCO-DB-Animator-ID"


class AP_AnimatorAssignedVillageAdmin(admin.ModelAdmin):
    list_display = ['id', 'animator', 'village', 'user_created', 'time_created']
    search_fields = ['animator']


class JSLPS_AnimatorAdmin(admin.ModelAdmin):
    list_display = ('id','animator_code', 'user_created', 'time_created',
                    '_animator', 'activity')
    search_fields = ['id', 'animator_code']
    list_filter = ['activity']

    def _animator(self, obj):
        return "%s:%s" % (obj.animator.id, obj.animator.name)
    _animator.allow_tags = True
    _animator.short_description = "COCO-DB-Animator-ID"


class JSLPS_AnimatorAssignedVillageAdmin(admin.ModelAdmin):
    list_display = ['id', 'animator', 'village', 'user_created', 'time_created']
    search_fields = ['animator']


class JSLPS_PersongroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_code', 'user_created', 'time_created',
                    '_persongroup', 'activity']
    search_fields = ['group__group_name', 'group_code']
    list_filter = ['activity']

    def _persongroup(self, obj):
        return "%s:%s" % (obj.group.id, obj.group.group_name)
    _persongroup.allow_tags = True
    _persongroup.short_description = "COCO-DB-PersonGroup-ID"


class JSLPS_PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_code', 'person', '_group_code', 'user_created',
                    'time_created', 'activity', '_person', '_block_name']
    search_fields = ['id', 'person_code', 'person__id', 'group__group_code']
    list_filter = ['activity']

    def _person(self, obj):
        return "%s:%s" % (obj.person.id, obj.person.person_name)
    _person.allow_tags = True
    _person.short_description = "COCO-DB-Person-ID"

    def _group_code(self, obj):
        if obj.group:
            return "%s" % obj.group.group_code
        else:
            return  obj.group 
    _group_code.allow_tags = True
    _group_code.short_description = "PersonGroup-Code"

    def _block_name(self, obj):
        return obj.person.village.block.block_name
    _block_name.allow_tags = True
    _block_name.allow_description = "Block Name"


class JSLPS_DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'district_code', 'district_name', 'user_created',
                    'time_created', '_district', 'activity']
    search_fields = ['id', 'district_code', 'district_name', 'district__id']
    list_filter = ['activity']

    def _district(self, obj):
        return "%s:%s" % (obj.district.id, obj.district.district_name)
    _district.allow_tags = True
    _district.short_description = "COCO-DB-District-ID"


class JSLPS_BlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'block_code', 'block_name', 'district_code',
                    'user_created', 'time_created', '_block', 'activity']
    search_fields = ['id', 'block_code', 'block_name', 'block', 'district_code']
    list_filter = ['activity']

    def _block(self, obj):
        return "%s:%s" % (obj.block.id, obj.block.block_name)
    _block.allow_tags = True
    _block.short_description = "COCO-DB-Block-ID"


class JSLPS_VillageAdmin(admin.ModelAdmin):
    list_display = ['id', 'village_code', 'village_name', 'block_code',
                    'user_created', 'time_created', '_village', 'activity']
    search_fields = ['id', 'village_code', 'village_name', 'block_code', 'Village__id']
    list_filter = ['activity']
    readonly_fields = list_display

    def _village(self, obj):
        return "%s:%s" % (obj.Village.id, obj.Village.village_name)
    _village.allow_tags = True
    _village.short_description = "COCO-DB-Village-ID"

    def has_add_permission(self, request):
        return False


class JSLPS_VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'vc', 'title', 'user_created', 'time_created',
                    '_video', 'activity']
    search_fields = ['id', 'vc', 'title']
    list_filter = ['activity']
    readonly_fields = list_display

    def _video(self, obj):
        return "%s:%s" % (obj.video.id, obj.video.title)
    _video.allow_tags = True
    _video.short_description = "COCO-DB-Video-ID"

    def has_add_permission(self, request):
        return False


class AP_ScreeningAdmin(admin.ModelAdmin):
    list_display = ['id', 'screening_code', 'total_members',
                    'screening', 'no_of_male', 'no_of_female', '_dg_screening_id',
                    'user_created', 'time_created']
    search_fields = ['id', 'screening_code', 'screening__village__block__block_name']
    readonly_fields = list_display

    def _dg_screening_id(self, obj):
        return obj.screening.id


class AP_AdoptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'member_code', 'ap_video', 'ap_animator',
                    'adoption', 'date_of_adoption', 'user_created', 'time_created']
    search_fields = ['id', 'member_code', 'ap_video', 'ap_animator', 'adoption']
    list_filter = ['date_of_adoption']

    readonly_fields = list_display

    def has_add_permission(self, request):
        return False


class JSLPS_ScreeningAdmin(admin.ModelAdmin):
    list_display = ['id', 'screenig_code', 'activity', 
                    'screening', '_village', '_dg_screening_id',
                    'user_created', 'time_created']
    search_fields = ['id', 'screenig_code', 'activity', 'screening__village__block__block_name']
    list_filter = ['activity']
    readonly_fields = list_display

    def _dg_screening_id(self, obj):
        return obj.screening.id

    def _village(self, obj):
        return "%s: %s: %s" % (obj.screening.village.village_name,
                               obj.screening.village.block.block_name,
                               obj.screening.village.block.district.district_name)

    def has_add_permission(self, request):
        return False


class JSLPS_AdoptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'member_code', 'jslps_video', 'jslps_akmcode',
                    'adoption', 'jslps_date_of_adoption', 'user_created', 'time_created']
    search_fields = ['id', 'member_code', 'jslps_video', 'jslps_akmcode', 'jslps_akmcode', 'adoption']
    list_filter = ['jslps_date_of_adoption']

    readonly_fields = list_display

    def has_add_permission(self, request):
        return False

