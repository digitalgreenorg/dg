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
from geographies.models import District, Block, State
from models import QACocoUser, QAReviewerCategory, QAReviewerName, VideoContentApproval, VideoQualityReview, DisseminationQuality, AdoptionVerification
from forms import QACocoUserForm

class QACocoUserAdmin(admin.ModelAdmin):
    form = QACocoUserForm
    list_display = ('user', 'partner', 'get_districts')
    search_fields = ['user__username']

class VideoContentApprovalAdmin(admin.ModelAdmin):
    list_display = ('video', 'qareviewername')
    search_fields = ['video']

class VideoQualityReviewAdmin(admin.ModelAdmin):
    list_display=('video','qareviewername', 'total_score', 'video_grade')

class DisseminationQualityAdmin(admin.ModelAdmin):
    list_display = ('date', 'mediator','village', 'total_score', 'video_grade')
    search_fields = ['mediator']

class AdoptionVerificationAdmin(admin.ModelAdmin):
    list_display = ('verification_date','person','village', 'mediator')
    search_fields = ['verification_date']
    
class QAReviewerNameAdmin(admin.ModelAdmin):
    list_display = ('reviewer_category', 'name')
    search_fields = ['name']