from django.contrib import admin
from dg.dashboard.models import *

from django import forms
from django.contrib.contenttypes import generic


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



	
class FarmerAttendanceInline(admin.TabularInline):
    model = PersonMeetingAttendance
    extra = 2  

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
    farmer_groups_targeted = DynamicMultipleChoiceField(widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))
    #farmer_groups_targeted = forms.ModelMultipleChoiceField(queryset=PersonGroups.objects.none())
    animator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))
    
    #farmers_groups_targeted = forms.ModelChoiceField(PersonGroups.objects, widget=forms.SelectMultiple(attrs={'onchange':'filter_person();'}))


    class Meta:
	    model = Screening

		

   
	 	
class ScreeningAdmin(admin.ModelAdmin):
    fields = ('date','start_time','end_time','location','village','animator','videoes_screened','target_person_attendance','target_audience_interest','target_adoptions','fieldofficer','farmer_groups_targeted')
    inlines = [FarmerAttendanceInline]
    filter_horizontal = ('videoes_screened',)
    list_display = ('date', 'village', 'location')
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
		settings.ADMIN_MEDIA_PREFIX + "js/filter1.js",
		settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.core.js",
		settings.ADMIN_MEDIA_PREFIX + "js/ui/ui.sortable.js",
		settings.ADMIN_MEDIA_PREFIX + "js/dynamic_inlines_with_sort.js",
		#settings.ADMIN_MEDIA_PREFIX + "js/dynamicinline.js",
		settings.ADMIN_MEDIA_PREFIX + "js/filter_person.js",
	)

	css = {
		'all':('/media/css/dynamic_inlines_with_sort.css',)
	}
   	
class ReviewerInline(generic.GenericTabularInline):
	model = Reviewer


class DevelopmentManagerAdmin(admin.ModelAdmin):
	exclude = ('equipmentholder','salary')
	list_display = ('name','region')
	#inlines = [ReviewerInline, ]

class VideoForm(forms.ModelForm):
	class DynamicChoiceField(forms.ChoiceField):     
		def clean(self, value):         
			return value      

        facilitator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))
    	cameraoperator = forms.ModelChoiceField(Animator.objects, widget=forms.Select(attrs={'disabled': 'true'}))

	class Meta:
		model = Video


class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
		(None, {'fields':['title','video_type','video_production_start_date','video_production_end_date','language','storybase','summary']}),
		('Upload Files',{'fields':['storyboard_filename','raw_filename','movie_maker_project_filename','final_edited_filename']}),
		(None,{'fields':['village','facilitator','cameraoperator','related_agricultural_practices','farmers_shown','actors']}),
		('Video Quality', {'fields':['picture_quality','audio_quality','editing_quality','edit_start_date','edit_finish_date','thematic_quality']}),
		('Review', {'fields': ['reviewer','approval_date','supplementary_video_produced','video_suitable_for','remarks']}),
    ]
    filter_horizontal = ('related_agricultural_practices','farmers_shown',)
    list_display = ('id', 'title', 'village', 'video_production_start_date', 'video_production_end_date')
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
	fields = ('name','age','gender','csp_flag','camera_operator_flag','facilitator_flag','phone_no','address','partner','home_village')
	inlines = [AnimatorAssignedVillages]
	list_display = ('name', 'partner', 'home_village',)




class PersonGroupsInline(admin.TabularInline):
	model = PersonGroups
	extra = 5  

class AnimatorInline(admin.TabularInline):
	model = Animator
	extra = 5
	exclude = ('equipmentholder',)

class VillageAdmin(admin.ModelAdmin):
	list_display = ('village_name', 'block')
	inlines = [PersonGroupsInline, AnimatorInline]
	

class PersonInline(admin.TabularInline):
    model = Person
    exclude = ('equipmentholder',)
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
	form = PersonGroupsForm


class AnimatorAssignedVillageAdmin(admin.ModelAdmin):
	list_display = ('animator','village')


class FieldOfficerAdmin(admin.ModelAdmin):
	exclude = ('equipmentholder','reviewer','salary',)

class PartnersAdmin(admin.ModelAdmin):
	exclude = ('equipmentholder','reviewer',)


class PersonAdoptPracticeInline(admin.StackedInline):
	model = PersonAdoptPractice
	extra = 3

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
    exclude = ('equipmentholder',)

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
    animators_trained = forms.ModelMultipleChoiceField(Animator.objects, widget=forms.SelectMultiple(attrs={'disabled': 'true'}))
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
                settings.ADMIN_MEDIA_PREFIX + "js/animator_filter.js",
        )

class EquipmentAdmin(admin.ModelAdmin):
        list_display = ('equipment_type', 'model_no', 'serial_no')


admin.site.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Region)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(DevelopmentManager, DevelopmentManagerAdmin)
admin.site.register(FieldOfficer, FieldOfficerAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Partners, PartnersAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonGroups, PersonGroupsAdmin)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Language)
admin.site.register(Practices)
admin.site.register(Screening, ScreeningAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Equipment, EquipmentAdmin)
#admin.site.register(EquipmentHolder)
#admin.site.register(Reviewer)
#admin.site.register(Random)
#admin.site.register(Message, MessageAdmin)

