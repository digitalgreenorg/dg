from django.contrib import admin

class XMLSubmissionAdmin(admin.ModelAdmin):
    list_display = ('username', 'error_code', 'error_message', 'submission_time', 'xml_data')
    search_fields = ['username', 'xml_data', 'error_code', 'error_message']

class CommCareProjectAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['name', 'group_name', 'group_id']
                          }
                  )]
    list_display = ('name', 'group_name')
    search_fields = ['name']


class CommCareUserAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['username', 'guid', 'coco_user', 'project', 'mediator']
                          }
                  )]
    list_display = ('username', 'coco_user', 'project', 'mediator')
    search_fields = ['username']


class CommCareCaseAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['person', 'guid', 'project', 'user', 'is_open']
                          }
                  )]
    list_display = ('person', 'guid', 'is_open')
    search_fields = ['project__name']
