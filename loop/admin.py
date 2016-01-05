from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import *

class LoopAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

loop_admin = LoopAdmin(name='loop_admin')
loop_admin.register(Village)
loop_admin.register(Block)
loop_admin.register(District)
loop_admin.register(State)
loop_admin.register(Country)
loop_admin.register(LoopUser)
loop_admin.register(Crop)