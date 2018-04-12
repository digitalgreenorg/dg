# from django.contrib.admin.sites import AdminSite
# from dashboard.admin import JSLPS_AnimatorAdmin
# from dashboard.admin import JSLPS_AnimatorAssignedVillageAdmin
# from dashboard.admin import JSLPS_PersongroupAdmin
# from dashboard.admin import JSLPS_PersonAdmin
# from dashboard.admin import JSLPS_VillageAdmin
# from dashboard.admin import JSLPS_BlockAdmin
# from dashboard.admin import JSLPS_DistrictAdmin
# from dashboard.admin import JSLPS_VideoAdmin
# from dashboard.admin import JSLPS_ScreeningAdmin, JSLPS_AdoptionAdmin
# from geographies.models import JSLPS_Village
# from geographies.models import JSLPS_District
# from geographies.models import JSLPS_Block
# from videos.models import JSLPS_Video
# from activities.models import JSLPS_Screening, JSLPS_Adoption
# from people.models import JSLPS_Animator
# from people.models import JSLPS_AnimatorAssignedVillage
# from people.models import JSLPS_Persongroup
# from people.models import JSLPS_Person
#
#
# class JSLPSAdmin(AdminSite):
#
#     def has_permission(self, request):
#         return request.user.is_active
#
# jslps_admin = JSLPSAdmin(name="admin_jslps")
#
# jslps_admin.index_template = 'social_website/index.html'
# jslps_admin.login_template = 'social_website/login.html'
# jslps_admin.logout_template = 'social_website/home.html'
#
# jslps_admin.register(JSLPS_Video, JSLPS_VideoAdmin)
# jslps_admin.register(JSLPS_Screening, JSLPS_ScreeningAdmin)
# jslps_admin.register(JSLPS_Adoption, JSLPS_AdoptionAdmin)
# jslps_admin.register(JSLPS_Village, JSLPS_VillageAdmin)
# jslps_admin.register(JSLPS_District, JSLPS_DistrictAdmin)
# jslps_admin.register(JSLPS_Block, JSLPS_BlockAdmin)
# jslps_admin.register(JSLPS_Person, JSLPS_PersonAdmin)
# jslps_admin.register(JSLPS_Persongroup, JSLPS_PersongroupAdmin)
# jslps_admin.register(JSLPS_AnimatorAssignedVillage, JSLPS_AnimatorAssignedVillageAdmin)
# jslps_admin.register(JSLPS_Animator, JSLPS_AnimatorAdmin)
#
