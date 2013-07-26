from django.contrib import admin
from models import Partner

class PartnerAdmin(admin.ModelAdmin):

    fields = ['coco_id','name','description','location','joinDate','logoURL','websiteURL']
    
    list_display = ('coco_id','name','joinDate')
