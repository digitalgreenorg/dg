import operator

from django import forms
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import smart_str

from ajax_filtered_fields.forms import AjaxForeignKeyField, FilteredSelect

from activities.models import PersonMeetingAttendance, Screening, PersonAdoptPractice
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from dashboard.forms import CocoUserForm


class PersonMeetingAttendanceForm(forms.ModelForm):
    person = forms.ModelChoiceField(Animator.objects.none())
    class Meta:
        model = PersonMeetingAttendance

class FarmerAttendanceInline(admin.TabularInline):
    model = PersonMeetingAttendance
    raw_id_fields = ("person",)
    extra = 0


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

    #farmers_groups_targeted = forms.ModelChoiceField(PersonGroup.objects, widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))


    class Meta:
        model = Screening

class ScreeningAdmin(admin.ModelAdmin):
    inlines = [FarmerAttendanceInline,]
    filter_horizontal = ('videoes_screened',)
    list_display = ('date', 'village', 'location')
    search_fields = ['village__village_name']
    raw_id_fields = ('village', 'animator', 'farmer_groups_targeted', 'videoes_screened',)
        

class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
                (None, {'fields':['title','video_type','video_production_start_date','video_production_end_date','language','summary', 'partner', 'related_practice']}),
                (None,{'fields':['village','facilitator','cameraoperator','farmers_shown','actors']}),
                ('Review', {'fields': ['approval_date','video_suitable_for','youtubeid']}),
    ]
    list_display = ('id', 'title', 'village', 'video_production_start_date', 'video_production_end_date')
    search_fields = ['title', 'village__village_name']
    raw_id_fields = ('village', 'facilitator', 'cameraoperator', 'farmers_shown', 'related_practice')


class AnimatorAssignedVillages(admin.StackedInline):
    model = AnimatorAssignedVillage

class AnimatorAdmin(admin.ModelAdmin):
    fields = ('name','gender','phone_no','partner','district')
    inlines = [AnimatorAssignedVillages]
    list_display = ('name', 'partner', 'district',)
    search_fields = ['name', 'partner__partner_name']

class PersonGroupInline(admin.TabularInline):
    model = PersonGroup
    extra = 5

class AnimatorInline(admin.TabularInline):
    model = Animator
    extra = 5
    exclude = ('assigned_villages',)

class VillageAdmin(admin.ModelAdmin):
    list_display = ('village_name', 'block')
    search_fields = ['village_name', 'block__block_name']
    inlines = [PersonGroupInline, AnimatorInline]


class PersonInline(admin.TabularInline):
    model = Person
    extra = 30


class PersonGroupForm(forms.ModelForm):
    class Meta:
        model = PersonGroup

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
    list_display = ('date_of_adoption', '__unicode__')
    search_fields = ['person__person_name', 'person__village__village_name', 'video__title']
    raw_id_fields = ('person', 'video')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__')
    search_fields = ['person_name','village__village_name','group__group_name']


class BlockAdmin(admin.ModelAdmin):
    list_display = ('block_name', 'district')
    search_fields = ['block_name', 'district__district_name']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'state')
    search_fields = ['district_name', 'state__state_name']

class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name',)
    search_fields = ['state_name', 'country__country_name']

class PracticesAdmin(admin.ModelAdmin):
    list_display = ('id', 'practice_sector', 'practice_subject', 'practice_subsector', 'practice_topic', 'practice_subtopic')
    search_fields = ['id', 'practice_sector__name', 'practice_subject__name', 'practice_subsector__name', 'practice_topic__name', 'practice_subtopic__name']

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
