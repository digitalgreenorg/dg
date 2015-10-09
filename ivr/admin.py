from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import Call

class CallAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['exotel_call_id', 'attributes', 'state', 'time_created', 'time_updated']
                          }
                  )]
    list_display = ('exotel_call_id', 'attributes', 'state', 'time_created', 'time_updated')
    search_fields =['exotel_call_id']


# class IvrAdmin(AdminSite):
#     def has_permission(self, request):
#         return request.user.is_active


# ivr_admin = IvrAdmin(name='ivr_admin')
# ivr_admin.register(CallAdmin)
