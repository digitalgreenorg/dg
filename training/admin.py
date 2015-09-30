from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import Trainer, TrainingUser, Assessment, Question

class TrainingAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

training_admin = TrainingAdmin(name='training_admin')
training_admin.register(Trainer)
training_admin.register(TrainingUser)
training_admin.register(Assessment)
training_admin.register(Question)
