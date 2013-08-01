from communications.admin import Article, ArticleAdmin
from django.contrib.admin.sites import AdminSite
from human_resources.admin import MemberAdmin
from human_resources.models import Member
from social_website.admin import Activity, ActivityAdmin, Partner, PartnerAdmin

class WebsiteAdmin(AdminSite):
    pass

website_admin = WebsiteAdmin(name="admin_website")

website_admin.register(Activity, ActivityAdmin)
website_admin.register(Article, ArticleAdmin)
website_admin.register(Member, MemberAdmin)
website_admin.register(Partner, PartnerAdmin)