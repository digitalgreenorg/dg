from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin
from dashboard.admin import AnimatorAdmin, AnimatorAssignedVillageAdmin, BlockAdmin, CocoUserAdmin, DistrictAdmin, PersonAdmin, PersonAdoptPracticeAdmin, PersonGroupAdmin, PracticesAdmin, PracticeSectorAdmin, PracticeSubjectAdmin, PracticeSubSectorAdmin, PracticeSubtopicAdmin, PracticeTopicAdmin, ScreeningAdmin, StateAdmin, VideoAdmin, VillageAdmin

from activities.models import PersonAdoptPractice, Screening
from coco.models import CocoUser
from geographies.models import Block, Country, District, Region, State, Village
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from programs.models import Partner
from videos.models import Language, Practice, PracticeSector, PracticeSubject, PracticeSubSector, PracticeSubtopic, PracticeTopic,  Video


class CocoAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

coco_admin = CocoAdmin(name="admin_coco")

coco_admin.register(User, UserAdmin)
coco_admin.register(Group, GroupAdmin)

coco_admin.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
coco_admin.register(Video, VideoAdmin)
coco_admin.register(Region)
coco_admin.register(Country)
coco_admin.register(State, StateAdmin)
coco_admin.register(District, DistrictAdmin)
coco_admin.register(Block, BlockAdmin)
coco_admin.register(Village, VillageAdmin)
coco_admin.register(Partner)
coco_admin.register(Person, PersonAdmin)
coco_admin.register(PersonGroup, PersonGroupAdmin)
coco_admin.register(Animator, AnimatorAdmin)
coco_admin.register(Language)
coco_admin.register(Practice, PracticesAdmin)
coco_admin.register(Screening, ScreeningAdmin)
coco_admin.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
coco_admin.register(PracticeSector, PracticeSectorAdmin)
coco_admin.register(PracticeSubSector, PracticeSubSectorAdmin)
coco_admin.register(PracticeTopic, PracticeTopicAdmin)
coco_admin.register(PracticeSubtopic, PracticeSubtopicAdmin)
coco_admin.register(PracticeSubject, PracticeSubjectAdmin)
coco_admin.register(CocoUser, CocoUserAdmin)
#admin.register(Reviewer)
#admin.register(Random)
#admin.register(Message, MessageAdmin)
