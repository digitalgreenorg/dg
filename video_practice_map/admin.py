from django.contrib import admin
from video_practice_map.models import VideoPractice, SkippedVideo


class VideoPracticeAdmin(admin.ModelAdmin):
    search_fields = ['user__username','video__title']

class SkippedVideoAdmin(admin.ModelAdmin):
    search_fields = ['video__title','user__username']

admin.site.register(VideoPractice,VideoPracticeAdmin)
admin.site.register(SkippedVideo,SkippedVideoAdmin)
