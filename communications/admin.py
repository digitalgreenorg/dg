from django.contrib import admin
from models import Article

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['title', 'location', 'source',
                                     'content', 'pub_date', 
                                     'link']
                          }
                  )]
    list_display = ('title', 'pub_date', 'location')
    search_fields = ['title']
    list_filter = ['pub_date']
        