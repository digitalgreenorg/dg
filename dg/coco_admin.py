from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin
from dashboard.admin import AnimatorAdmin
from dashboard.admin import AnimatorAssignedVillageAdmin
from dashboard.admin import BlockAdmin
from dashboard.admin import CocoUserAdmin
from dashboard.admin import DistrictAdmin
from dashboard.admin import PersonAdmin
from dashboard.admin import PersonAdoptPracticeAdmin
from dashboard.admin import PersonGroupAdmin
from dashboard.admin import PracticesAdmin
from dashboard.admin import PracticeSectorAdmin
from dashboard.admin import PracticeSubjectAdmin
from dashboard.admin import PracticeSubSectorAdmin
from dashboard.admin import PracticeSubtopicAdmin
from dashboard.admin import PracticeTopicAdmin
from dashboard.admin import ScreeningAdmin
from dashboard.admin import StateAdmin
from dashboard.admin import VideoAdmin
from dashboard.admin import VillageAdmin
from dashboard.admin import SubCategoryAdmin
from dashboard.admin import VideoPracticeAdmin
from dashboard.admin import ParentCategoryAdmin
from dashboard.admin import ProjectAdmin
from dashboard.admin import TagAdmin
from dashboard.admin import PartnerAdmin
from activities.models import PersonAdoptPractice, Screening
from coco.models import CocoUser
from geographies.models import Block, Country, District, State, Village
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from programs.models import Partner
from programs.models import Project
from videos.models import Language
from videos.models import Practice
from videos.models import PracticeSector
from videos.models import PracticeSubject
from videos.models import PracticeSubSector
from videos.models import PracticeSubtopic
from videos.models import PracticeTopic
from videos.models import Video
from videos.models import Category
from videos.models import SubCategory
from videos.models import VideoPractice
from videos.models import Tag
from videos.models import ParentCategory


class CocoAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

coco_admin = CocoAdmin(name="admin_coco")

coco_admin.index_template = 'social_website/index.html'
coco_admin.login_template = 'social_website/login.html'
coco_admin.logout_template = 'social_website/home.html'

coco_admin.register(User, UserAdmin)
coco_admin.register(Group, GroupAdmin)

coco_admin.register(AnimatorAssignedVillage, AnimatorAssignedVillageAdmin)
coco_admin.register(Video, VideoAdmin)
coco_admin.register(Country)
coco_admin.register(State, StateAdmin)
coco_admin.register(District, DistrictAdmin)
coco_admin.register(Block, BlockAdmin)
coco_admin.register(Village, VillageAdmin)
coco_admin.register(Partner, PartnerAdmin)
coco_admin.register(Project, ProjectAdmin)
coco_admin.register(Person, PersonAdmin)
coco_admin.register(PersonGroup, PersonGroupAdmin)
coco_admin.register(Animator, AnimatorAdmin)
coco_admin.register(Language)
coco_admin.register(Category)
coco_admin.register(SubCategory, SubCategoryAdmin)
coco_admin.register(VideoPractice, VideoPracticeAdmin)
coco_admin.register(Tag, TagAdmin)
coco_admin.register(Practice, PracticesAdmin)
coco_admin.register(Screening, ScreeningAdmin)
coco_admin.register(ParentCategory, ParentCategoryAdmin)
coco_admin.register(PersonAdoptPractice, PersonAdoptPracticeAdmin)
coco_admin.register(PracticeSector, PracticeSectorAdmin)
coco_admin.register(PracticeSubSector, PracticeSubSectorAdmin)
coco_admin.register(PracticeTopic, PracticeTopicAdmin)
coco_admin.register(PracticeSubtopic, PracticeSubtopicAdmin)
coco_admin.register(PracticeSubject, PracticeSubjectAdmin)
coco_admin.register(CocoUser, CocoUserAdmin)
