from django.conf.urls.defaults import *
from website.api import VideoResource, LanguageResource, CountryResource, FarmerResource, ActivityResource, CollectionResource, PartnerResource, CommentResource
from website.user_api import SignInResource, UserCollectionHistoryResource, VideoLikeResource, CommentLikeResource, UserResource
video_resource = VideoResource()
language_resource = LanguageResource()
country_resource = CountryResource()
farmer_resource = FarmerResource()
activity_resource = ActivityResource()
collection_resource = CollectionResource()
partner_resource = PartnerResource()
comment_resource = CommentResource()
# following added for user based information
signin_resource = SignInResource()
usercollectionhistory_resource = UserCollectionHistoryResource()
videolike_resource = VideoLikeResource()
commentlike_resource = CommentLikeResource()
user_resource = UserResource()



urlpatterns = patterns('',
    (r'v1/', include(video_resource.urls)),
    (r'v1/', include(language_resource.urls)),
    (r'v1/', include(country_resource.urls)),
    (r'v1/', include(farmer_resource.urls)),
    (r'v1/', include(activity_resource.urls)),
    (r'v1/', include(collection_resource.urls)),
    (r'v1/', include(partner_resource.urls)),
    (r'v1/', include(comment_resource.urls)),
    (r'v1/', include(signin_resource.urls)),
    (r'v1/', include(usercollectionhistory_resource.urls)),
    (r'v1/', include(videolike_resource.urls)),
    (r'v1/', include(commentlike_resource.urls)),
    (r'v1/', include(user_resource.urls)),
    
)