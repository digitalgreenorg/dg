from django.contrib.admin.sites import AdminSite

from communications.admin import Article, ArticleAdmin
from human_resources.admin import JobAdmin, MemberAdmin
from human_resources.models import Job, Member
from social_website.admin import Activity, ActivityAdmin, Collection, CollectionAdmin, FeaturedCollection, FeaturedCollectionAdmin, Partner, PartnerAdmin

class WebsiteAdmin(AdminSite):
    pass

website_admin = WebsiteAdmin(name="admin_website")

website_admin.register(Activity, ActivityAdmin)
website_admin.register(Article, ArticleAdmin)
website_admin.register(Collection, CollectionAdmin)
website_admin.register(FeaturedCollection, FeaturedCollectionAdmin)
website_admin.register(Job, JobAdmin)
website_admin.register(Member, MemberAdmin)
website_admin.register(Partner, PartnerAdmin)