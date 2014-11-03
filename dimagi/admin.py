from django.contrib import admin

class XMLSubmissionAdmin(admin.ModelAdmin):
    list_display = ('username', 'error_code', 'error_message', 'submission_time', 'xml_data')
    search_fields = ['username', 'xml_data', 'error_code', 'error_message']

class CommCareProjectAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['name']
                          }
                  )]
    list_display = ('name',)
    search_fields = ['name']


class CommCareUserAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['project', 'coco_user']
                          }
                  )]
    list_display = ('username', 'project', 'guid')
    search_fields = ['username']


class CommCareCaseAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['person', 'guid', 'project', 'user', 'is_open']
                          }
                  )]
    list_display = ('person', 'guid', 'is_open')
