# from django.contrib.admin.sites import AdminSite

# from communications.admin import Article, ArticleAdmin, Feedback, FeedbackAdmin
# from social_website.admin import Collection, CollectionAdmin, FeaturedCollection, FeaturedCollectionAdmin, Partner, PartnerAdmin, ResourceVideo, ResourceVideoAdmin


# class WebsiteAdmin(AdminSite):
#
#     def has_permission(self, request):
#         return request.user.is_active

# website_admin = WebsiteAdmin(name="admin_website")
#
# website_admin.index_template = 'social_website/index.html'
# website_admin.login_template = 'social_website/login.html'
# website_admin.logout_template = 'social_website/home.html'
#
# # website_admin.register(Activity, ActivityAdmin)
# # website_admin.register(Feedback, FeedbackAdmin)
# # website_admin.register(Article, ArticleAdmin)
# website_admin.register(Collection, CollectionAdmin)
# website_admin.register(FeaturedCollection, FeaturedCollectionAdmin)
# # website_admin.register(Geography, GeographyAdmin)
# # website_admin.register(Job, JobAdmin)
# # website_admin.register(Member, MemberAdmin)
# website_admin.register(Partner, PartnerAdmin)
# # website_admin.register(Place, PlaceAdmin)
# website_admin.register(ResourceVideo, ResourceVideoAdmin)
