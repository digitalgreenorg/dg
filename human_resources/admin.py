from django.contrib import admin
#from forms import ImageAdminForm
from models import Geography, ExperienceQualification, Job, KeyResponsibility

class MemberAdmin(admin.ModelAdmin):
    #form = ImageAdminForm
    fieldsets = [(None,  {'fields': ['name', 'email', 'designation',
                                     'team', 'personal_intro', 'location',
                                     'image', 'hierarchy_num']
                          }
                  )]
    list_display = ('name', 'email', 'designation')
    search_fields = ['name']

class KeyResponsibilityInline(admin.TabularInline):
    model = KeyResponsibility
    extra = 10
        
class ExperienceQualificationInline(admin.TabularInline):
    model = ExperienceQualification
    extra = 10
    
class JobAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['title','description','conclusion','hierarchy_num', 'geography']})]
    inlines = [ExperienceQualificationInline, KeyResponsibilityInline]
    list_display = ('hierarchy_num','title', 'geography')
    search_fields = ['title']

class GeographyAdmin(admin.ModelAdmin):
    fieldsets = [(None, { 'fields': ['name', 'description', 'hierarchy_number']})]
    list_display = ('name', 'hierarchy_number', )
