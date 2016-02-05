from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from models import *

class LoopAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ['name', 'phone']


#class CombinedTransactionAdmin(admin.ModelAdmin):
#    list_display = ('id', 'date', 'price', 'quantity', 'amount', 'status')
#    search_fields = ['farmer__name','crop__crop_name','mandi__mandi_name','status']
#    list_filter = ('status', 'farmer__village__village_name')


loop_admin = LoopAdmin(name='loop_admin')
loop_admin.register(Village)
loop_admin.register(Block)
loop_admin.register(District)
loop_admin.register(State)
loop_admin.register(Country)
loop_admin.register(LoopUser)
loop_admin.register(Crop)
loop_admin.register(Farmer, FarmerAdmin)
loop_admin.register(CombinedTransaction)
loop_admin.register(Mandi)
