from django.contrib.admin.sites import AdminSite
from social_website.admin import PartnerAdmin
from social_website.admin import Partner

class WebsiteAdmin(AdminSite):
    pass

website_admin = WebsiteAdmin(name="media")

website_admin.register(Partner, PartnerAdmin)