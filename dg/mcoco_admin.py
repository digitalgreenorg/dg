from django.contrib.admin.sites import AdminSite

from dimagi.models import *
from dimagi.admin import *

class McocoAdmin(AdminSite):
    pass

mcoco_admin = McocoAdmin(name="admin_mcoco")

mcoco_admin.register(CommCareProject, CommCareProjectAdmin)
mcoco_admin.register(CommCareUser, CommCareUserAdmin)
mcoco_admin.register(CommCareUserVillage, CommCareUserVillageAdmin)
mcoco_admin.register(CommCareCase, CommCareCaseAdmin)
