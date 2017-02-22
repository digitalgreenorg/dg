from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import Trainer, TrainingUser, Assessment, Question, LogData

class TrainingAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'section','serial','tag')
    search_fields = ['assessment__name', 'section','serial']
    list_filter = ['assessment__name','tag']

class TrainerAdmin(admin.ModelAdmin):
	list_display = ('id','name','email')

training_admin = TrainingAdmin(name='training_admin')
training_admin.register(Trainer, TrainerAdmin)
training_admin.register(TrainingUser)
training_admin.register(Assessment)
training_admin.register(Question, QuestionAdmin)
training_admin.register(LogData)
