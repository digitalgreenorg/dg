from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

#from qacoco.admin import VideoContentApprovalAdmin

from qacoco.models import QACocoUser, QAReviewer, VideoContentApproval


class QACocoAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

qacoco_admin = QACocoAdmin(name="admin_qacoco")

qacoco_admin.register(QAReviewer)
qacoco_admin.register(VideoContentApproval)
qacoco_admin.register(QACocoUser)