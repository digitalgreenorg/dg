from django.contrib.admin.sites import AdminSite
from human_resources.admin import MemberAdmin
from human_resources.models import Member
from social_website.admin import PartnerAdmin, Partner

class WebsiteAdmin(AdminSite):
    pass

website_admin = WebsiteAdmin(name="admin_website")

website_admin.register(Member, MemberAdmin)
website_admin.register(Partner, PartnerAdmin)