from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from models import Trainer, TrainingUser, Assessment, Question, LogData
from geographies.models import State

class TrainingUserForm(forms.ModelForm):
    states = forms.ModelMultipleChoiceField(
        queryset=State.objects.all(),
        widget=FilteredSelectMultiple("States", is_stacked=False),
        label='States')

class TrainingAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

class TrainingUserAdmin(admin.ModelAdmin):
	form = TrainingUserForm

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'section','serial','tag')
    search_fields = ['assessment__name', 'section','serial']
    list_filter = ['assessment__name','tag']

class TrainerAdmin(admin.ModelAdmin):
	list_display = ('id','name','email')

training_admin = TrainingAdmin(name='training_admin')
training_admin.register(Trainer, TrainerAdmin)
training_admin.register(TrainingUser,TrainingUserAdmin)
training_admin.register(Assessment)
training_admin.register(Question, QuestionAdmin)
training_admin.register(LogData)
