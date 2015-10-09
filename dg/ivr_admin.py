from django.contrib.admin.sites import AdminSite

from ivr.models import Call
from ivr.admin import CallAdmin

class IvrAdmin(AdminSite):
    pass

ivr_admin = IvrAdmin(name="ivrsadmin")

ivr_admin.register(Call, CallAdmin)
