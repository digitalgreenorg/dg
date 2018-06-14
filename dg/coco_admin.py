from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

class CocoAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

coco_admin = CocoAdmin(name="admin_coco")

coco_admin.index_template = 'social_website/index.html'
coco_admin.login_template = 'social_website/login.html'
coco_admin.logout_template = 'social_website/home.html'

coco_admin.register(User, UserAdmin)
coco_admin.register(Group, GroupAdmin)

