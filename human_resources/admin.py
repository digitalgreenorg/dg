from django.contrib import admin
from forms import ImageAdminForm

class MemberAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    fieldsets = [(None,  {'fields': ['name', 'email', 'designation',
                                     'team', 'personal_intro', 'location',
                                     'image']
                          }
                  )]
    list_display = ('name', 'email', 'designation')
    search_fields = ['name']
