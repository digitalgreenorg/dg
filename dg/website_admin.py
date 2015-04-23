from django.contrib.admin.sites import AdminSite

from communications.admin import Article, ArticleAdmin
from human_resources.admin import GeographyAdmin, JobAdmin, MemberAdmin, PlaceAdmin
from human_resources.models import Geography, Job, Member, Place
from social_website.admin import Activity, ActivityAdmin, Collection, CollectionAdmin, FeaturedCollection, FeaturedCollectionAdmin, Partner, PartnerAdmin, ResourceVideo, ResourceVideoAdmin


class WebsiteAdmin(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

website_admin = WebsiteAdmin(name="admin_website")

website_admin.register(Activity, ActivityAdmin)
website_admin.register(Article, ArticleAdmin)
website_admin.register(Collection, CollectionAdmin)
website_admin.register(FeaturedCollection, FeaturedCollectionAdmin)
website_admin.register(Geography, GeographyAdmin)
website_admin.register(Job, JobAdmin)
website_admin.register(Member, MemberAdmin)
website_admin.register(Partner, PartnerAdmin)
website_admin.register(Place, PlaceAdmin)
website_admin.register(ResourceVideo, ResourceVideoAdmin)