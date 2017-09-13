from django.contrib.admin.sites import AdminSite

from dimagi.models import CommCareCase, CommCareProject, CommCareUser, XMLSubmission
from dimagi.admin import CommCareCaseAdmin, CommCareProjectAdmin, CommCareUserAdmin, XMLSubmissionAdmin

class McocoAdmin(AdminSite):
    pass

mcoco_admin = McocoAdmin(name="admin_mcoco")

mcoco_admin.index_template = 'social_website/index.html'
mcoco_admin.login_template = 'social_website/login.html'
mcoco_admin.logout_template = 'social_website/home.html'

mcoco_admin.register(CommCareProject, CommCareProjectAdmin)
mcoco_admin.register(CommCareUser, CommCareUserAdmin)
mcoco_admin.register(CommCareCase, CommCareCaseAdmin)
mcoco_admin.register(XMLSubmission, XMLSubmissionAdmin)