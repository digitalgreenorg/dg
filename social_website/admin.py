from django.contrib import admin
from models import Activity, Collection, FeaturedCollection, Partner, VideoinCollection, ResourceVideo

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


class VideoCollectionInline(admin.TabularInline):
    model = VideoinCollection


class CollectionAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['title', 'thumbnailURL', 'country', 'state', 'partner', 'language', 'category', 'subcategory', 'topic', 'subtopic', 'subject', 'featured', 'description']
                          }
                  )]
    inlines = [VideoCollectionInline,]
    list_display = ('title', 'category', 'partner', 'country', 'state', 'language')
    search_fields = ['title', 'partner__name', 'country', 'state', 'language']
    filter_horizontal = ('videos',)

class FeaturedCollectionAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['collageURL', 'collection', 'show_on_homepage', 'show_on_language_selection']
                          }
                  )]
    list_display = ('collection', 'collageURL')
    search_fields = ['collection']

class ResourceVideoAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['title', 'youtubeID', 'videoTag', 'date']
                          }
                  )]
    list_display = ('title', 'youtubeID', 'videoTag', 'date')
    search_fields = ['title', 'youtubeID', 'videoTag']
