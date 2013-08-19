from django.contrib import admin
from models import Activity, Collection, FeaturedCollection, Partner

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
    
class CollectionAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['title', 'thumbnailURL', 'state', 'partner', 'language', 'videos', 'category', 'subcategory', 'topic', 'subtopic', 'subject', 'likes', 'views', 'adoptions']
                          }
                  )]
    list_display = ('title', 'category', 'partner', 'state', 'language')
    search_fields = ['title']
    
class FeaturedCollectionAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['collageURL','collection']
                          }
                  )]
    list_display = ('collection', 'collageURL')
    search_fields = ['collection']