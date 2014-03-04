from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

from dashboard.admin import AnimatorAdmin, AnimatorAssignedVillageAdmin, BlockAdmin, CocoUserAdmin, DevelopmentManagerAdmin, DistrictAdmin, EquipmentAdmin, FieldOfficerAdmin, PersonAdmin, PersonAdoptPracticeAdmin, PersonGroupsAdmin, PracticesAdmin, PracticeSectorAdmin, PracticeSubjectAdmin, PracticeSubSectorAdmin, PracticeSubtopicAdmin, PracticeTopicAdmin, ScreeningAdmin, StateAdmin, TargetAdmin, TrainingAdmin, UserPermissionAdmin, VideoAdmin, VillageAdmin

from dashboard.models import Animator, AnimatorAssignedVillage, Block, CocoUser, Country, DevelopmentManager, District, Equipment, EquipmentHolder, FieldOfficer, Language, Partners, Person, PersonAdoptPractice, PersonGroups, Practices, PracticeSector, PracticeSubject, PracticeSubSector, PracticeSubtopic, PracticeTopic, Region, State, Screening, Target, Training, UserPermission, Video, Village

from video_practice_map.admin import SkippedVideoAdmin, VideoPracticeAdmin
from video_practice_map.models import SkippedVideo, VideoPractice

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
admin.register(DevelopmentManager, DevelopmentManagerAdmin)
admin.register(FieldOfficer, FieldOfficerAdmin)
admin.register(Village, VillageAdmin)
admin.register(Partners)
admin.register(Person, PersonAdmin)
admin.register(PersonGroups, PersonGroupsAdmin)
admin.register(Animator, AnimatorAdmin)
admin.register(Language)
admin.register(Practices, PracticesAdmin)
admin.register(Screening, ScreeningAdmin)
admin.register(Training, TrainingAdmin)
admin.register(Equipment, EquipmentAdmin)
admin.register(Target, TargetAdmin)
admin.register(UserPermission, UserPermissionAdmin)
admin.register(EquipmentHolder)
admin.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
admin.register(PracticeSector, PracticeSectorAdmin)
admin.register(PracticeSubSector, PracticeSubSectorAdmin)
admin.register(PracticeTopic, PracticeTopicAdmin)
admin.register(PracticeSubtopic, PracticeSubtopicAdmin)
admin.register(PracticeSubject, PracticeSubjectAdmin)
admin.register(CocoUser, CocoUserAdmin)

admin.register(VideoPractice, VideoPracticeAdmin)
admin.register(SkippedVideo, SkippedVideoAdmin)
