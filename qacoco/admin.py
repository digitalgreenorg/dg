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
from forms import QACocoUserForm

class QACocoUserAdmin(admin.ModelAdmin):
    form = QACocoUserForm
    list_display = ('user', 'partner', 'get_districts')
    search_fields = ['user__username']

class VideoQualityReviewAdmin(admin.ModelAdmin):
    list_display=('video','qareviewername', 'total_score', 'video_grade')
    raw_id_fields = ('video')

class DisseminationQualityAdmin(admin.ModelAdmin):
    list_display = ('date', 'mediator','village', 'total_score', 'video_grade')
    search_fields = ['mediator']
    raw_id_fields = ('block', 'village', 'mediator', 'video')

class AdoptionNonNegotiableVerfication(admin.StackedInline):
    model = AdoptionNonNegotiableVerfication

class AdoptionVerificationAdmin(admin.ModelAdmin):
    list_display = ('verification_date','person','village', 'mediator')
    search_fields = ['verification_date']
    raw_id_fields = ('block', 'village', 'mediator', 'person', 'group', 'video')
    inlines = [AdoptionNonNegotiableVerfication]
    
class QAReviewerNameAdmin(admin.ModelAdmin):
    list_display = ('reviewer_category', 'name')
    search_fields = ['name']

class VideoAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

class VillageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

class BlockAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

class AnimatorAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

class PersonAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

class PersonGroupAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}
