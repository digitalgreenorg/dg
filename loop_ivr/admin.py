from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import SimpleListFilter

from loop_ivr.models import PriceInfoIncoming, PriceInfoLog, Subscriber, Subscription, \
	SubscriptionLog

class LoopIVRAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

class PriceInfoIncomingAdmin(admin.ModelAdmin):
    list_filter = ['info_status', 'call_source', 'to_number', 'incoming_time']
    search_fields = ['from_number']
    list_display = ('id' ,'call_id', 'from_number', 'to_number', 'incoming_time', 'call_source', 'info_status', 'query_code', 'prev_info_status', 'prev_query_code','server_response_time')

class PriceInfoLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'price_info_incoming', 'crop', 'mandi')

class SubscriberAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'phone_no', 'type_of_subscriber', 'status')

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'subscriber', 'start_date', 'subscription_code', 'status')

class SubscriptionLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'subscription', 'date', 'sms_id', 'status')

loop_ivr_admin = LoopIVRAdmin(name='loop_ivr_admin')

loop_ivr_admin.index_template = 'social_website/index.html'
loop_ivr_admin.login_template = 'social_website/login.html'
loop_ivr_admin.logout_template = 'social_website/home.html'

loop_ivr_admin.register(PriceInfoIncoming, PriceInfoIncomingAdmin)
loop_ivr_admin.register(PriceInfoLog, PriceInfoLogAdmin)
loop_ivr_admin.register(Subscriber, SubscriberAdmin)
loop_ivr_admin.register(Subscription, SubscriptionAdmin)
loop_ivr_admin.register(SubscriptionLog, SubscriptionLogAdmin)
