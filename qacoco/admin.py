import operator

from django import forms
from django.conf import settings
from django.conf.urls import patterns
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import smart_str
from django.forms import TextInput, Textarea
from videos.models import Video
from geographies.models import State, District, Block, Village
from people.models import Animator, PersonGroup, Person
from models import QACocoUser, QAReviewerCategory, QAReviewerName, VideoQualityReview, DisseminationQuality, AdoptionVerification, AdoptionNonNegotiableVerfication
from forms import QACocoUserForm, DisseminationQualityAdminForm

class QACocoUserAdmin(admin.ModelAdmin):
    # For use custom QACocoUserForm 
    form = QACocoUserForm
    list_display = ('user', 'partner', 'get_blocks')
    search_fields = ['user__username']
    #filter_horizontal = ('blocks','videos')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return QACocoUser.objects.all()
        return QACocoUser.objects.filter(user=request.user)

    def get_readonly_fields(self, request, obj=None):
         self.readonly_fields = []
         if not request.user.is_superuser:
            self.readonly_fields = ['user', 'partner', 'blocks',]
         return self.readonly_fields

class VideoQualityReviewAdmin(admin.ModelAdmin):
    list_display=('video', 'qareviewername', 'total_score', 'video_grade')
    raw_id_fields = ('video')

class DisseminationQualityAdmin(admin.ModelAdmin):
    form = DisseminationQualityAdminForm
    list_display = ('date', 'mediator','village', 'total_score', 'video_grade')
    search_fields = ['mediator', 'village', 'total_score', 'video_grade']
    raw_id_fields = ('block', 'village', 'mediator', 'video')

    # So the form can have access to the request
    # def get_form(self, request, obj=None, **kwargs):
    #     # Pass the request object to the form
    #     form = super(DisseminationQualityAdmin, self).get_form(request, obj, **kwargs)
    #     form.request = request
    #     return form

class AdoptionNonNegotiableVerfication(admin.StackedInline):
    model = AdoptionNonNegotiableVerfication

class AdoptionVerificationAdmin(admin.ModelAdmin):
    list_display = ('verification_date', 'person', 'village', 'mediator')
    search_fields = ['verification_date', 'person', 'village', 'mediator']
    raw_id_fields = ('block', 'village', 'mediator', 'person', 'group', 'video')
    inlines = [AdoptionNonNegotiableVerfication]

class QAReviewerNameAdmin(admin.ModelAdmin):
    list_display = ('reviewer_category', 'name')
    search_fields = ['reviewer_category', 'name']

# class VideoAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}

# class VillageAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}

# class BlockAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}

# class AnimatorAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}

# class PersonAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}

# class PersonGroupAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}
