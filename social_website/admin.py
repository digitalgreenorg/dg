from django.contrib import admin
from models import Partner, Activity

class PartnerAdmin(admin.ModelAdmin):

    fields = ['coco_id','name','full_name','description','location','joinDate','logoURL','location_image','websiteURL']
    
    list_display = ('coco_id','name','joinDate')

class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['title', 'date', 'textContent', 'newsFeed']
                          }
                  )]
    list_display = ('title', 'date', 'textContent')
    search_fields = ['title']
    list_filter = ['date']
    