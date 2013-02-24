from django.contrib import admin
from dashboard.models import *

from django import forms
from django.contrib.contenttypes import generic


# django-ajax filtered fields
from ajax_filtered_fields.forms import AjaxForeignKeyField
from django.conf import settings
from ajax_filtered_fields.forms import FilteredSelect



# autocomplete widget
import operator
from django.db import models
#from django.contrib.auth.models import Message
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str

from dashboard.widgets import ForeignKeySearchInput, MonthYearWidget
from django.conf.urls.defaults import *

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
    farmer_groups_targeted = forms.ModelMultipleChoiceField(PersonGroups.objects, widget=forms.SelectMultiple(attrs={'onchange': 'filter_person();'}))
    #farmer_groups_targeted = DynamicMultipleChoiceField(widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))
    #farmer_groups_targeted = forms.ModelMultipleChoiceField(queryset=PersonGroups.objects.none())
    #animator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))
    animator = forms.ModelChoiceField(Animator.objects)

    #farmers_groups_targeted = forms.ModelChoiceField(PersonGroups.objects, widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))


    class Meta:
        model = Screening

class ScreeningAdmin(admin.ModelAdmin):
    fields = ('date','start_time','end_time','location','village','animator','target_person_attendance','target_audience_interest','farmer_groups_targeted','videoes_screened','target_adoptions','fieldofficer',)
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
                settings.ADMIN_MEDIA_PREFIX + "js/jquery-1.3.2.min.js",
                                settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.core.js",
                settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.sortable.js",
                settings.ADMIN_MEDIA_PREFIX + "js/screening_page.js",
                #settings.ADMIN_MEDIA_PREFIX + "js/dynamicinline.js",

        )

        css = {
                'all':('/media/css/screening_page.css',)
        }

class ReviewerInline(generic.GenericTabularInline):
    model = Reviewer


class DevelopmentManagerAdmin(admin.ModelAdmin):
    exclude = ('salary',)
    list_display = ('name','region')
    #inlines = [ReviewerInline, ]

class VideoForm(forms.ModelForm):
    class DynamicChoiceField(forms.ChoiceField):
        def clean(self, value):
            return value

    facilitator = forms.ModelChoiceField(Animator.objects, widget=forms.Select())
    cameraoperator = forms.ModelChoiceField(Animator.objects, widget=forms.Select())

    class Meta:
        model = Video


class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
                (None, {'fields':['title','video_type','video_production_start_date','video_production_end_date','language','storybase','summary']}),
                ('Upload Files',{'fields':['storyboard_filename','raw_filename','movie_maker_project_filename','final_edited_filename']}),
                (None,{'fields':['village','facilitator','cameraoperator','farmers_shown','actors']}),
                ('Video Quality', {'fields':['picture_quality','audio_quality','editing_quality','edit_start_date','edit_finish_date','thematic_quality']}),
                ('Review', {'fields': ['reviewer','approval_date','supplementary_video_produced','video_suitable_for','remarks','youtubeid']}),
    ]
    list_display = ('id', 'title', 'village', 'video_production_start_date', 'video_production_end_date')
    search_fields = ['title', 'village__village_name']
    #raw_id_fields = ('village',)
    #form = VideoForm
    related_search_fields = {
        'village': ('village_name',),
    }

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
        return super(VideoAdmin, self).__call__(request, url)

    def get_urls(self):
        urls = super(VideoAdmin,self).get_urls()
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
        return super(VideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    form = VideoForm

    class Media:
        js = (
                settings.ADMIN_MEDIA_PREFIX + "js/jquery-1.3.2.min.js",
                settings.ADMIN_MEDIA_PREFIX + "js/video_filter.js",
        )



class AnimatorAssignedVillages(admin.StackedInline):
    model = AnimatorAssignedVillage

class AnimatorAdmin(admin.ModelAdmin):
    fields = ('name','age','gender','csp_flag','camera_operator_flag','facilitator_flag','phone_no','address','partner','village')
    inlines = [AnimatorAssignedVillages]
    list_display = ('name', 'partner', 'village',)
    search_fields = ['name','village__village_name', 'partner__partner_name']

class PersonGroupsInline(admin.TabularInline):
    model = PersonGroups
    extra = 5

class AnimatorInline(admin.TabularInline):
    model = Animator
    extra = 5
    exclude = ('assigned_villages',)

class VillageAdmin(admin.ModelAdmin):
    list_display = ('village_name', 'block')
    search_fields = ['village_name', 'block__block_name']
    inlines = [PersonGroupsInline, AnimatorInline]


class PersonInline(admin.TabularInline):
    model = Person
    extra = 30


class PersonGroupsForm(forms.ModelForm):
    class Meta:
        model = PersonGroups

    class Media:
        js = (
                settings.ADMIN_MEDIA_PREFIX + "js/filter_village.js",
                #settings.ADMIN_MEDIA_PREFIX + "js/jquery-1.3.2.min.js",
                #settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.core.js",
                #settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.sortable.js",
                #settings.ADMIN_MEDIA_PREFIX + "js/dynamic_inlines_with_sort.js",
        )

        #css = {
        #        'all':('/media/css/dynamic_inlines_with_sort.css',)
        #}



class PersonGroupsAdmin(admin.ModelAdmin):
    inlines = [PersonInline]
    list_display = ('group_name','village')
    search_fields = ['group_name','village__village_name']
    form = PersonGroupsForm


class AnimatorAssignedVillageAdmin(admin.ModelAdmin):
    list_display = ('animator','village')
    search_fields = ['animator__name','village__village_name']

class FieldOfficerAdmin(admin.ModelAdmin):
    exclude = ('salary',)

class PersonAdoptPracticeInline(admin.StackedInline):
    model = PersonAdoptPractice
    extra = 3

class PersonAdoptPracticeAdmin(admin.ModelAdmin):
    list_display = ('person',)
    search_fields = ['person__person_name','person__village__village_name',]

class PersonForm(forms.ModelForm):
    class DynamicChoiceField(forms.ChoiceField):
        def clean(self, value):
            return value

    #group = DynamicChoiceField(widget=forms.Select(attrs={'disabled': 'true'}))

    #group = forms.ModelChoiceField(PersonGroups.objects, widget=forms.Select(attrs={'disabled': 'true'}))

    class Meta:
        model = Person


class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonAdoptPracticeInline]
    list_display = ('person_name','group','village')
    exclude = ('date_of_joining',)
    search_fields = ['person_name','village__village_name','group__group_name']
    related_search_fields = {
        'village': ('village_name',),
    }

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
        return super(PersonAdmin, self).__call__(request, url)

    def get_urls(self):
        urls = super(PersonAdmin,self).get_urls()
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
        return super(PersonAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    form = PersonForm

    class Media:
        js = (
                settings.ADMIN_MEDIA_PREFIX + "js/jquery-1.3.2.min.js",
                settings.ADMIN_MEDIA_PREFIX + "js/person_filter.js",
        )


class BlockAdmin(admin.ModelAdmin):
    list_display = ('block_name', 'district')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'state','fieldofficer', 'partner')

class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'region')

class TrainingForm(forms.ModelForm):
    animators_trained = forms.ModelMultipleChoiceField(Animator.objects, widget=forms.SelectMultiple())
    class Meta:
        model = Training

class TrainingAdmin(admin.ModelAdmin):
    list_display = ('training_start_date', 'training_end_date', 'village')
    filter_horizontal = ('animators_trained',)
    related_search_fields = {
        'village': ('village_name',),
    }

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
        return super(TrainingAdmin, self).__call__(request, url)

    def get_urls(self):
        urls = super(TrainingAdmin,self).get_urls()
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
        return super(TrainingAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    form = TrainingForm

    class Media:
        js = (
                settings.ADMIN_MEDIA_PREFIX + "js/jquery-1.3.2.min.js",
        )

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_type', 'model_no', 'invoice_no', 'village', 'equipmentholder', 'procurement_date', 'remarks')
    
    def district_name(self, obj):
      return ("%s" % (obj.village.block.district.district_name)).title()
    district_name.short_description = 'District'


class PracticesAdmin(admin.ModelAdmin):
    search_fields = ['practice_name']

class UserPermissionAdmin(admin.ModelAdmin):
	list_display = ('username','role','region_operated','district_operated')

class TargetAdmin(admin.ModelAdmin):

    formfield_overrides = {
    models.DateField: {'widget': MonthYearWidget},
}
    fieldsets = [
    (None, {
        'fields': ['month_year', 'district']
    }),
    ('New Villages', {
       'fields': ['clusters_identification', 'dg_concept_sharing', 'csp_identification', 'dissemination_set_deployment']
    }),
    (None, {
       'fields': ['village_operationalization']
    }),
    ('Videos', {
       'fields': ['video_uploading', 'video_production', 'storyboard_preparation', 'video_shooting', 'video_editing', 'video_quality_checking']
    }),
    ('Disseminations', {
       'fields': ['disseminations', 'avg_attendance_per_dissemination', 'exp_interest_per_dissemination', 'adoption_per_dissemination']
    }),
    ('Training', {
       'fields': ['crp_training', 'crp_refresher_training', 'csp_training', 'csp_refresher_training', 'editor_training', 'editor_refresher_training']
    }),
    (None, {
       'fields': ['villages_certification']
    }),
    ('Qualitative Feedback', {
       'fields': ['what_went_well', 'what_not_went_well', 'challenges', 'support_requested']
    }),
]

    list_display = ('month_year','district')

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

admin.site.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(DevelopmentManager, DevelopmentManagerAdmin)
admin.site.register(FieldOfficer, FieldOfficerAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Partners)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonGroups, PersonGroupsAdmin)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Language)
admin.site.register(Practices, PracticesAdmin)
admin.site.register(Screening, ScreeningAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(UserPermission, UserPermissionAdmin)
admin.site.register(EquipmentHolder)
admin.site.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
admin.site.register(PracticeSector,PracticeSectorAdmin)
admin.site.register(PracticeSubSector,PracticeSubSectorAdmin)
admin.site.register(PracticeTopic,PracticeTopicAdmin)
admin.site.register(PracticeSubtopic,PracticeSubtopicAdmin)
admin.site.register(PracticeSubject,PracticeSubjectAdmin)
#admin.site.register(Reviewer)
#admin.site.register(Random)
#admin.site.register(Message, MessageAdmin)
