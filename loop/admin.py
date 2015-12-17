from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import Upload

class LoopAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

loop_admin = LoopAdmin(name='loop_admin')
loop_admin.register(Upload)
