from django.contrib import admin
from models import Article, Feedback

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['title', 'location', 'source',
                                     'content', 'pub_date', 
                                     'link']
                          }
                  )]
    list_display = ('title', 'pub_date', 'location')
    search_fields = ['title']
    list_filter = ['pub_date']
        
class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['rating', 'comments', 'email']
                          }
                  )]
    list_display = ('rating', 'comments', 'email', 'time')
    search_fields = ['email']
    list_filter = ['date']
