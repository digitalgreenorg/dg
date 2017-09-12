from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

from qacoco.models import QACocoUser, QAReviewerCategory,QAReviewerName, VideoQualityReview, DisseminationQuality, AdoptionVerification
from videos.models import Video
from geographies.models import State, District, Block, Village
from people.models import Animator, Person, PersonGroup

from qacoco.admin import QACocoUserAdmin, QAReviewerNameAdmin, VideoQualityReviewAdmin, DisseminationQualityAdmin, AdoptionVerificationAdmin, VideoAdmin, VillageAdmin, BlockAdmin, AnimatorAdmin, PersonGroupAdmin, PersonAdmin


class QACocoAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

qacoco_admin = QACocoAdmin(name="admin_qacoco")

qacoco_admin.index_template = 'social_website/index.html'
qacoco_admin.login_template = 'social_website/login.html'
qacoco_admin.logout_template = 'social_website/home.html'

qacoco_admin.register(QAReviewerCategory)
qacoco_admin.register(QAReviewerName, QAReviewerNameAdmin)
qacoco_admin.register(QACocoUser, QACocoUserAdmin)
qacoco_admin.register(VideoQualityReview, VideoQualityReviewAdmin)
qacoco_admin.register(DisseminationQuality, DisseminationQualityAdmin)
qacoco_admin.register(AdoptionVerification, AdoptionVerificationAdmin)
qacoco_admin.register(Video, VideoAdmin)
qacoco_admin.register(Village, VillageAdmin)
qacoco_admin.register(Block, VideoAdmin)
qacoco_admin.register(Animator, VillageAdmin)
qacoco_admin.register(Person, PersonAdmin)
qacoco_admin.register(PersonGroup, PersonGroupAdmin)
