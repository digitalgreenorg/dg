from django.contrib.admin.sites import AdminSite
from social_website.admin import PartnerAdmin, Partner

class WebsiteAdmin(AdminSite):
    pass

website_admin = WebsiteAdmin(name="admin_website")

website_admin.register(Partner, PartnerAdmin)