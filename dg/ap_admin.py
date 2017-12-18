from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin
from videos.models import APVideo
from dashboard.admin import APVideoAdmin



class APAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

ap_admin = APAdmin(name="admin_ap")

ap_admin.index_template = 'social_website/index.html'
ap_admin.login_template = 'social_website/login.html'
ap_admin.logout_template = 'social_website/home.html'


ap_admin.register(APVideo, APVideoAdmin)