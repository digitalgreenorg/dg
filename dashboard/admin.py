import operator

from django import forms
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import smart_str

# django-ajax filtered fields
from ajax_filtered_fields.forms import AjaxForeignKeyField
from ajax_filtered_fields.forms import FilteredSelect

from activities.models import *
from coco.models import *
from geographies.models import *
from programs.models import *
from people.models import *
from videos.models import *
from dashboard.widgets import ForeignKeySearchInput, MonthYearWidget

from forms import CocoUserForm

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
    fields = ('date','start_time','end_time','location','partner','village','animator','target_person_attendance','target_audience_interest','farmer_groups_targeted','videoes_screened','target_adoptions','fieldofficer',)
    inlines = [FarmerAttendanceInline,]
    filter_horizontal = ('videoes_screened',)
    list_display = ('date', 'village', 'location')
    search_fields = ['village__village_name']
    #form = ScreeningForm
    related_search_fields = {
        'village': ('village_name',),
    }

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
        return super(ScreeningAdmin, self).__call__(request, url)

    def get_urls(self):
        urls = super(ScreeningAdmin,self).get_urls()
        search_url = patterns('',
        (r'^search/$', self.search)
        )
        return search_url + urls

    def search(self, request):
        """
        Searches in the fields of the given related model and returns the
        result as a simple string to be used by the jQuery Autocomplete plugin
        """
        query = request.GET.get('q', None)
        app_label = request.GET.get('app_label', None)
        model_name = request.GET.get('model_name', None)
        search_fields = request.GET.get('search_fields', None)

        if search_fields and app_label and model_name and query:
            def construct_search(field_name):
        # use different lookup methods depending on the notation
                if field_name.startswith('^'):
                    return "%s__istartswith" % field_name[1:]
                elif field_name.startswith('='):
                    return "%s__iexact" % field_name[1:]
                elif field_name.startswith('@'):
                    return "%s__search" % field_name[1:]
                else:
                    return "%s__icontains" % field_name

            model = models.get_model(app_label, model_name)
            qs = model._default_manager.all()
            for bit in query.split():
                or_queries = [models.Q(**{construct_search(
                    smart_str(field_name)): smart_str(bit)})
                        for field_name in search_fields.split(',')]
                other_qs = QuerySet(model)
                other_qs.dup_select_related(qs)
                other_qs = other_qs.filter(reduce(operator.or_, or_queries))
                qs = qs & other_qs
            data = ''.join([u'%s|%s\n' % (f.__unicode__(), f.pk) for f in qs])
            return HttpResponse(data)
        return HttpResponseNotFound()

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overrides the default widget for Foreignkey fields if they are
        specified in the related_search_fields class attribute.
        """
        if isinstance(db_field, models.ForeignKey) and \
                db_field.name in self.related_search_fields:
            kwargs['widget'] = ForeignKeySearchInput(db_field.rel,
                                    self.related_search_fields[db_field.name])
        return super(ScreeningAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    form = ScreeningForm

    class Media:
        js = (
                settings.STATIC_URL + "js/jquery-1.3.2.min.js",
                                settings.STATIC_URL + "js/ui/ui.core.js",
                settings.STATIC_URL + "js/ui/ui.sortable.js",
                settings.STATIC_URL + "js/screening_page.js",
                #settings.STATIC_URL + "js/dynamicinline.js",

        )

        css = {
                'all':('/media/css/screening_page.css',)
        }

class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
                (None, {'fields':['title','video_type','video_production_start_date','video_production_end_date','language','storybase','summary', 'partner', 'related_practice']}),
                ('Upload Files',{'fields':['storyboard_filename','raw_filename','movie_maker_project_filename','final_edited_filename']}),
                (None,{'fields':['village','facilitator','cameraoperator','farmers_shown','actors']}),
                ('Video Quality', {'fields':['picture_quality','audio_quality','editing_quality','edit_start_date','edit_finish_date','thematic_quality']}),
                ('Review', {'fields': ['approval_date','supplementary_video_produced','video_suitable_for','remarks','youtubeid']}),
    ]
    list_display = ('id', 'title', 'village', 'video_production_start_date', 'video_production_end_date')
    search_fields = ['title', 'village__village_name']
    raw_id_fields = ('village', 'facilitator', 'cameraoperator', 'farmers_shown', 'related_practice')


class AnimatorAssignedVillages(admin.StackedInline):
    model = AnimatorAssignedVillage

class AnimatorAdmin(admin.ModelAdmin):
    fields = ('name','age','gender','csp_flag','camera_operator_flag','facilitator_flag','phone_no','address','partner','district')
    inlines = [AnimatorAssignedVillages]
    list_display = ('name', 'partner', 'district',)
    search_fields = ['name','village__village_name', 'partner__partner_name']

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

class FieldOfficerAdmin(admin.ModelAdmin):
    exclude = ('salary',)

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
    list_display = ('district_name', 'state', 'partner')
    search_fields = ['district_name', 'state__state_name']

class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'region')
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

admin.site.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Partner)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonGroup, PersonGroupAdmin)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Language)
admin.site.register(Practice, PracticesAdmin)
admin.site.register(Screening, ScreeningAdmin)
admin.site.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
admin.site.register(PracticeSector,PracticeSectorAdmin)
admin.site.register(PracticeSubSector,PracticeSubSectorAdmin)
admin.site.register(PracticeTopic,PracticeTopicAdmin)
admin.site.register(PracticeSubtopic,PracticeSubtopicAdmin)
admin.site.register(PracticeSubject,PracticeSubjectAdmin)
admin.site.register(CocoUser, CocoUserAdmin)
#admin.site.register(Reviewer)
#admin.site.register(Random)
#admin.site.register(Message, MessageAdmin)
