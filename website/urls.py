from django.conf.urls.defaults import *
from website.api import VideoResource, LanguageResource, CountryResource, FarmerResource, ActivityResource, CollectionResource, PartnerResource, InterestResource, CommentResource

video_resource = VideoResource()
language_resource = LanguageResource()
country_resource = CountryResource()
farmer_resource = FarmerResource()
activity_resource = ActivityResource()
collection_resource = CollectionResource()
partner_resource = PartnerResource()
interest_resource = InterestResource()
comment_resource = CommentResource()
urlpatterns = patterns('',
    (r'v1/', include(video_resource.urls)),
    (r'v1/', include(language_resource.urls)),
    (r'v1/', include(country_resource.urls)),
    (r'v1/', include(farmer_resource.urls)),
    (r'v1/', include(activity_resource.urls)),
    (r'v1/', include(collection_resource.urls)),
    (r'v1/', include(partner_resource.urls)),
    (r'v1/', include(interest_resource.urls)),
    (r'v1/', include(comment_resource.urls)),
)