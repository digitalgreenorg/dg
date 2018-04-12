from django.contrib.admin.sites import AdminSite
from videos.models import APVideo
from geographies.models import AP_District
from geographies.models import AP_Mandal
from geographies.models import AP_Village
from geographies.models import AP_Habitation
from people.models import AP_Person
from people.models import AP_Animator
from activities.models import AP_Screening
from activities.models import AP_Adoption
from videos.models import APCrop
from videos.models import APPractice
from people.models import AP_AnimatorAssignedVillage
from dashboard import AP_HabitationAdmin
from dashboard import APVideoAdmin
from dashboard import AP_DistrictAdmin
from dashboard import AP_VillageAdmin
from dashboard import AP_BlockAdmin
from dashboard import AP_PersonAdmin
from dashboard import AP_AnimatorAssignedVillageAdmin
from dashboard import AP_AnimatorAdmin
from dashboard import APCropAdmin
from dashboard import APPracticeAdmin
from dashboard import AP_ScreeningAdmin
from dashboard import AP_AdoptionAdmin




class APAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

ap_admin = APAdmin(name="admin_ap")

ap_admin.index_template = 'social_website/index.html'
ap_admin.login_template = 'social_website/login.html'
ap_admin.logout_template = 'social_website/home.html'

ap_admin.register(AP_Adoption, AP_AdoptionAdmin)
ap_admin.register(AP_Screening, AP_ScreeningAdmin)
ap_admin.register(APPractice, APPracticeAdmin)
ap_admin.register(APCrop, APCropAdmin)
ap_admin.register(AP_Animator, AP_AnimatorAdmin)
ap_admin.register(AP_AnimatorAssignedVillage, AP_AnimatorAssignedVillageAdmin)
ap_admin.register(AP_Person, AP_PersonAdmin)
ap_admin.register(AP_Habitation, AP_HabitationAdmin)
ap_admin.register(AP_Village, AP_VillageAdmin)
ap_admin.register(AP_Mandal, AP_BlockAdmin)
ap_admin.register(AP_District, AP_DistrictAdmin)
ap_admin.register(APVideo, APVideoAdmin)
# ap_admin.register(BluefrogSubcategory, BluefrogSubcategoryAdmin)
# ap_admin.register(BluefrogPractice, BluefrogPracticeAdmin)
# ap_admin.register(DistrictScreening, DistrictScreeningAdmin)