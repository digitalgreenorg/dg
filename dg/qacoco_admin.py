from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

#from qacoco.admin import VideoContentApprovalAdmin

from qacoco.models import QACocoUser, QAReviewerCategory,QAReviewerName, VideoContentApproval, VideoQualityReview, DisseminationQuality, AdoptionVerification
from qacoco.admin import QACocoUserAdmin, QAReviewerNameAdmin, VideoContentApprovalAdmin, VideoQualityReviewAdmin, DisseminationQualityAdmin, AdoptionVerificationAdmin

class QACocoAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

qacoco_admin = QACocoAdmin(name="admin_qacoco")

qacoco_admin.register(QAReviewerCategory)
qacoco_admin.register(QAReviewerName, QAReviewerNameAdmin)
qacoco_admin.register(QACocoUser, QACocoUserAdmin)
qacoco_admin.register(VideoContentApproval, VideoContentApprovalAdmin)
qacoco_admin.register(VideoQualityReview, VideoQualityReviewAdmin)
qacoco_admin.register(DisseminationQuality, DisseminationQualityAdmin)
qacoco_admin.register(AdoptionVerification, AdoptionVerificationAdmin)