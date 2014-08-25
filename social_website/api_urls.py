from django.conf.urls import include, patterns, url
from elastic_search import get_collections_from_elasticsearch, searchCompletions
from social_website.api import VideoLikeResource, UserResource, VideoResource, PersonResource, ActivityResource, CollectionResource, PartnerResource, CommentResource, PartnerFarmerResource
from views import searchFilters, featuredCollection, mapping


video_resource = VideoResource()
farmer_resource = PersonResource()
activity_resource = ActivityResource()
collection_resource = CollectionResource()
partner_resource = PartnerResource()
comment_resource = CommentResource()
partnerfarmer_resource = PartnerFarmerResource()

user_resource = UserResource()
videolike_resource = VideoLikeResource()

urlpatterns = patterns('',
    (r'^api/', include(video_resource.urls)),
    (r'^api/', include(farmer_resource.urls)),
    (r'^api/', include(activity_resource.urls)),
    (r'^api/', include(collection_resource.urls)),
    (r'^api/', include(partner_resource.urls)),
    (r'^api/', include(comment_resource.urls)),
    (r'^api/', include(partnerfarmer_resource.urls)),
    (r'^api/searchCompletions?$',searchCompletions),
    (r'^api/searchFilters$', searchFilters),
    (r'^api/elasticSearch/$', get_collections_from_elasticsearch),
    (r'^api/featuredCollection/$', featuredCollection),
    (r'^api/', include(videolike_resource.urls)),
    (r'^api/', include(user_resource.urls)),
    (r'^api/mapping/$', mapping),

#    (r'', include(signin_resource.urls)),
#    (r'', include(usercollectionhistory_resource.urls)),
#    (r'', include(videolike_resource.urls)),
#    (r'', include(commentlike_resource.urls)),
#    (r'', include(user_resource.urls)),
#    (r'', include(partnerfarmer_resource.urls)),
)