from django.contrib import admin
from dg.dashboard.models import *

from django import forms


# django-ajax filtered fields
from ajax_filtered_fields.forms import AjaxForeignKeyField
from django.conf import settings
from ajax_filtered_fields.forms import FilteredSelect



# autocomplete widget 
import operator
from django.db import models
from django.contrib.auth.models import Message
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str

from dg.dashboard.widgets import ForeignKeySearchInput
from django.conf.urls.defaults import *


class MyDMForm(forms.ModelForm):
        # lookups explained below
        #region = AjaxForeignKeyField(Region, (('region_name',{}),),default_index=0, select_related= None, widget=FilteredSelect(attrs={'onchange':'temp();'}))
	region = AjaxForeignKeyField(Region, (('region_name',{}),),default_index=0, select_related=None)

        class Meta:
            model = DevelopmentManager

        class Media:
            js = (
                settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
                settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
                settings.ADMIN_MEDIA_PREFIX + "js/jquery.js",
                settings.ADMIN_MEDIA_PREFIX + "js/ajax_filtered_fields.js",
		settings.ADMIN_MEDIA_PREFIX + "js/temp.js",
            )

#class VideoForm(forms.ModelForm):
#	village = forms.ModelChoiceField(Village.objects, widget=forms.Select)
#	#facilitator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))
#	facilitator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))
#
#	class Meta:
#		model = Video
#	
#	class Media:
#		js = (
#			settings.ADMIN_MEDIA_PREFIX + "js/dynamicselect.js",
#			settings.ADMIN_MEDIA_PREFIX + "js/jquery.js",
#		)
#

class VideoForm(forms.ModelForm):
	class DynamicChoiceField(forms.ChoiceField):     
		def clean(self, value):         
			return value      

	village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'FilterAnimators();'}))     
	facilitator = DynamicChoiceField(widget=forms.Select(attrs={'disabled':'true'}), choices=(('-1','Select Village'),))

	class Meta:
		model = Video

	class Media:
		js = (
			settings.ADMIN_MEDIA_PREFIX + "js/FilterAnimators.js",
			settings.ADMIN_MEDIA_PREFIX + "js/prototype.js",
		)
	

class ScreeningForm(forms.ModelForm):
	class DynamicChoiceField(forms.ChoiceField):     
		def clean(self, value):         
			return value      

	#village  = AjaxForeignKeyField(Village, (('village_name',{}),),default_index=0, select_related= None, widget=FilteredSelect(attrs={'onchange':'temp();'}))
	village = forms.ModelChoiceField(Village.objects, widget=forms.Select(attrs={'onchange':'temp();'}))
	#village = forms.ModelChoiceField(Village.objects, widget=forms.HiddenInput(attrs={'onchange':'temp();'}))
	animator = DynamicChoiceField(widget=forms.Select(attrs={'disabled': 'true'}), choices=(('-1','Select Village'),))

	class Meta:
		model = Screening

	class Media:
		js = (
			settings.ADMIN_MEDIA_PREFIX + "js/jquery-1.3.2.min.js",
			settings.ADMIN_MEDIA_PREFIX + "js/filter1.js",
			settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.core.js",
			settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.sortable.js",
			settings.ADMIN_MEDIA_PREFIX + "js/dynamic_inlines_with_sort.js",
		)

		css = {
			'all':('/media/css/dynamic_inlines_with_sort.css',)
		}



class DevelopmentManagerAdmin(admin.ModelAdmin):
    #form = MyDMForm
    related_search_fields = {
       	'region': ('region_name',),
    }

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
	print 'helllo'
        return super(DevelopmentManagerAdmin, self).__call__(request, url)

    def get_urls(self):
	urls = super(DevelopmentManagerAdmin,self).get_urls()
	search_url = patterns('',
	(r'^search/$', self.search)
	)
	print 'Hello'
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
        return super(DevelopmentManagerAdmin, self).formfield_for_dbfield(db_field, **kwargs)



class VideoAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['title','video_type','video_production_start_date','video_production_end_date','language','storybase','summary']}),
		('Upload Files',{'fields':['storyboard_filename','raw_filename','movie_maker_project_filename','final_edited_filename']}),
		(None,{'fields':['village','facilitator','cameraoperator','related_agricultural_practices','farmers_shown','actors']}),
		('Video Quality', {'fields':['picture_quality','audio_quality','editing_quality','edit_start_date','edit_finish_date','thematic_quality']}),
		('Review', {'fields': ['reviewer','approval_date','supplementary_video_produced','video_suitable_for','remarks']}),
	]
	filter_horizontal = ('related_agricultural_practices','farmers_shown',)
	#raw_id_fields = ('village',)
	form = VideoForm

class FarmerAttendanceInline(admin.TabularInline):
    model = PersonMeetingAttendance
    extra = 1  


class ScreeningAdmin(admin.ModelAdmin):
    fields = ('date','start_time','end_time','location','village','animator','videoes_screened','target_person_attendance','target_audience_interest','target_adoptions','fieldofficer','farmer_groups_targeted')
    inlines = [FarmerAttendanceInline]
    filter_horizontal = ('farmer_groups_targeted','videoes_screened',)
    list_display = ('date', 'village', 'location')
    related_search_fields = {
       	'fieldofficer': ('name',),
    }
    form = ScreeningForm

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
	print 'helllo'
        return super(ScreeningAdmin, self).__call__(request, url)

    def get_urls(self):
	urls = super(ScreeningAdmin,self).get_urls()
	search_url = patterns('',
	(r'^search/$', self.search)
	)
	print 'Hello'
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
                                    self.related_search_fields[db_field.name], attrs={'onchange':'temp();'})
        return super(ScreeningAdmin, self).formfield_for_dbfield(db_field, **kwargs)

   

class AnimatorAssignedVillages(admin.StackedInline):
	model = AnimatorAssignedVillage
	
class AnimatorAdmin(admin.ModelAdmin):
	fields = ('name','age','gender','csp_flag','camera_operator_flag','facilitator_flag','phone_no','address','partner','home_village')
	inlines = [AnimatorAssignedVillages]
	
admin.site.register(AnimatorAssignedVillage)
admin.site.register(Video, VideoAdmin)
admin.site.register(Region)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Block)
admin.site.register(DevelopmentManager, DevelopmentManagerAdmin)
admin.site.register(FieldOfficer)
admin.site.register(Village)
admin.site.register(Partners)
admin.site.register(Person)
admin.site.register(PersonGroups)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Language)
admin.site.register(Practices)
admin.site.register(Screening, ScreeningAdmin)
admin.site.register(Random)
#admin.site.register(Message, MessageAdmin)

