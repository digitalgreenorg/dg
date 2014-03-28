from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

from dashboard.admin import AnimatorAdmin, AnimatorAssignedVillageAdmin, BlockAdmin, CocoUserAdmin, DistrictAdmin, PersonAdmin, PersonAdoptPracticeAdmin, PersonGroupAdmin, PracticesAdmin, PracticeSectorAdmin, PracticeSubjectAdmin, PracticeSubSectorAdmin, PracticeSubtopicAdmin, PracticeTopicAdmin, ScreeningAdmin, StateAdmin, VideoAdmin, VillageAdmin

from activities.models import PersonAdoptPractice, Screening
from coco.models import CocoUser
from geographies.models import Block, Country, District, Region, State, Village
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from programs.models import Partner
from videos.models import Language, Practice, PracticeSector, PracticeSubject, PracticeSubSector, PracticeSubtopic, PracticeTopic,  Video


class Admin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

admin = Admin(name="admin")

admin.register(User, UserAdmin)
admin.register(Group, GroupAdmin)

admin.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
admin.register(Video, VideoAdmin)
admin.register(Region)
admin.register(Country)
admin.register(State, StateAdmin)
admin.register(District, DistrictAdmin)
admin.register(Block, BlockAdmin)
admin.register(Village, VillageAdmin)
admin.register(Partner)
admin.register(Person, PersonAdmin)
admin.register(PersonGroup, PersonGroupAdmin)
admin.register(Animator, AnimatorAdmin)
admin.register(Language)
admin.register(Practice, PracticesAdmin)
admin.register(Screening, ScreeningAdmin)
admin.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
admin.register(PracticeSector, PracticeSectorAdmin)
admin.register(PracticeSubSector, PracticeSubSectorAdmin)
admin.register(PracticeTopic, PracticeTopicAdmin)
admin.register(PracticeSubtopic, PracticeSubtopicAdmin)
admin.register(PracticeSubject, PracticeSubjectAdmin)
admin.register(CocoUser, CocoUserAdmin)
#admin.register(Reviewer)
#admin.register(Random)
#admin.register(Message, MessageAdmin)
