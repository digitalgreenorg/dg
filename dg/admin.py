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

admin.site.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Partner)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonGroup, PersonGroupAdmin)
admin.site.register(Animator, AnimatorAdmin)
admin.site.register(Language)
admin.site.register(Practice, PracticesAdmin)
admin.site.register(Screening, ScreeningAdmin)
admin.site.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
admin.site.register(PracticeSector, PracticeSectorAdmin)
admin.site.register(PracticeSubSector, PracticeSubSectorAdmin)
admin.site.register(PracticeTopic, PracticeTopicAdmin)
admin.site.register(PracticeSubtopic, PracticeSubtopicAdmin)
admin.site.register(PracticeSubject, PracticeSubjectAdmin)
admin.site.register(CocoUser, CocoUserAdmin)
#admin.site.register(Reviewer)
#admin.site.register(Random)
#admin.site.register(Message, MessageAdmin)
