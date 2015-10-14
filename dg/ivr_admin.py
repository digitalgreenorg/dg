from django.contrib.admin.sites import AdminSite

from ivr.models import Call, Broadcast
from ivr.admin import CallAdmin, BroadcastAdmin

class IvrAdmin(AdminSite):
    pass

ivr_admin = IvrAdmin(name="ivrsadmin")

ivr_admin.register(Call, CallAdmin)
ivr_admin.register(Broadcast, BroadcastAdmin)
