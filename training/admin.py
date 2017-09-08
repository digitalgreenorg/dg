from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from models import Trainer, TrainingUser, Assessment, Question, LogData, DeleteLog, Training
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
	list_display = ('id', 'user','assigned_states')

	def assigned_states(self,obj):
		return " , ".join([s.state_name for s in obj.states.all()])

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'section','serial','tag','__assessment__')
    search_fields = ['assessment__name', 'section','serial']
    list_filter = ['assessment__name','section','serial']

class TrainerAdmin(admin.ModelAdmin):
	list_display = ('id','name','email')

class LogDataAdmin(admin.ModelAdmin):
	actions = None
	list_display = ('id','entry_table','model_id','action','user')
	search_fields = ('entry_table','action','user')
	list_filter = ('entry_table','action')
	list_display_links = None

class DeleteLogAdmin(admin.ModelAdmin):
	actions = None
	list_display = ('id','entry_table','table_object')
	search_fields = ['entry_table']
	list_filter = ['entry_table']
	list_display_links = None

class TrainingListAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id','date','place','trainers','assessment','language','district','trainingType','kind_of_training','participants_count','partner')
    list_filter = ['assessment','language','partner']
    date_hierarchy = 'date'
    list_display_links = None

training_admin = TrainingAdmin(name='training_admin')

training_admin.index_template = 'social_website/index.html'
training_admin.login_template = 'social_website/login.html'
training_admin.logout_template = 'social_website/home.html'

training_admin.register(Trainer, TrainerAdmin)
training_admin.register(TrainingUser,TrainingUserAdmin)
training_admin.register(Assessment)
training_admin.register(Question, QuestionAdmin)
training_admin.register(LogData, LogDataAdmin)
training_admin.register(DeleteLog, DeleteLogAdmin)
training_admin.register(Training, TrainingListAdmin)
