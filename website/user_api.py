from tastypie.resources import ModelResource
from tastypie import fields
from website.user_models import CommentLike, TimeWatched, VideoLike, UserCollectionHistory
from django.contrib.auth.models import User
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from website.api import CollectionResource, VideoResource, CommentResource
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import BasicAuthentication, Authentication


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        
class SignInResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'signIn'
        filtering = {
           "username": ALL,
           "password": ALL,
        }
        
        
class UserCollectionHistoryResource(ModelResource):
    completed = fields.ManyToManyField(CollectionResource, 'completed')
    viewed = fields.ManyToManyField(CollectionResource, 'recentlyViewed')
    liked = fields.ManyToManyField(CollectionResource, 'likedCollections')
    class Meta:
        queryset = UserCollectionHistory.objects.all()
        resource_name = 'userCollectionHistory'
        filtering = {
           "userUID": ALL,
        }
        
class VideoLikeResource(ModelResource):
    video = fields.ForeignKey(VideoResource, 'videoUID')
    user = fields.ForeignKey(UserResource,'userUID')
    class Meta:
        queryset = VideoLike.objects.all()
        resource_name = 'updateVideoLike'
        authentication = Authentication()
        authorization = Authorization()

class CommentLikeResource(ModelResource):
    comment = fields.ForeignKey(CommentResource, 'commentUID')
    user = fields.ForeignKey(UserResource,'userUID')
    class Meta:
        queryset = CommentLike.objects.all()
        resource_name = 'updateCommentLike'
        authentication = Authentication()
        authorization = Authorization()
#class TimeWatchedResource(ModelResource):
#    class Meta:
#        queryset = TimeWatched.objects.all()
#        resource_name = 'updateTimeWatched'