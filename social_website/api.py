import datetime

from tastypie.resources import ModelResource
from tastypie import fields
from social_website.models import Activity, Collection, Comment, ImageSpec, Partner, Person, Video, UserProfile, VideoinCollection, VideoLike
from functools import partial
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from django.http import HttpResponse
from functools import partial
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import BasicAuthentication, Authentication

def many_to_many_to_subfield(bundle, field_name, sub_field_names):
    sub_fields = getattr(bundle.obj, field_name).values(*sub_field_names)
    return list(sub_fields)

def dict_to_foreign_uri(bundle, field_name, resource_name=None):
    print bundle.data
    field_dict = bundle.data.get(field_name)
    print field_dict
    bundle.data[field_name] = "/social/api/%s/%s/"%(resource_name if resource_name else field_name, 
                                                    str(field_dict))
    return bundle


class BaseCorsResource(ModelResource):
    """
    Class implementing CORS
    """
    def create_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
 
    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []
 
        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))
 
        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)
 
        '''if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)'''
 
        return request_method

class BaseResource(BaseCorsResource):
    class Meta:
        resource_name = 'base'
    def dehydrate(self, bundle):
        return bundle

class ImageSpecResource(BaseResource):
    class Meta:
        queryset = ImageSpec.objects.all()
        resource_name = 'imagespec'
        
class PartnerResource(BaseResource):
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'
        excludes = ['videos', 'likes', 'views', 'adoptions', 'badges']

class PersonResource(BaseResource):
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'person'

class PartnerFarmerResource(BaseResource):
    farmer = fields.ToManyField('social_website.api.PersonResource', 'person_set', full=True)
    dehydrate_farmer = partial(many_to_many_to_subfield, field_name='person_set',sub_field_names=['uid','coco_id','name','thumbnailURL'])
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partnerFarmers'
        fields=['person','name','uid','coco_id']
        filtering={
                   'uid':ALL
                   }

class VideoResource(BaseResource):
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True)
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
        excludes = ['category','subcategory','topic','subtopic','subject','state']
        filtering={
                   'uid':ALL,
                   'partner':ALL_WITH_RELATIONS,
                   'language':ALL,
                   'state':ALL,
                   }

    def dehydrate(self, bundle):
        video = bundle.obj
        tags = [x for x in [video.category,video.subcategory,video.topic,video.subtopic,video.subject] if x is not u'']
        bundle.data['tags'] = ','.join(tags)
        return bundle
 
class CollectionResource(BaseCorsResource):
    videos = fields.ListField()
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True)
    hydrate_partner = partial(dict_to_foreign_uri, field_name='partner', resource_name='partner')
    class Meta:
        always_return_data = True
        queryset = Collection.objects.all()
        resource_name = 'collections'
        excludes = ['category','subcategory','topic','subtopic','subject']
        ordering={'likes','views','adoptions'}
        authentication = Authentication()
        authorization = Authorization()
    
    def obj_create(self, bundle, **kwargs):
        video_list = bundle.data.get('videos')
        print video_list
        if video_list:
            bundle = super(CollectionResource, self).obj_create(bundle, **kwargs)
            print bundle
            print bundle.obj
            collection_id = getattr(bundle.obj,'uid')
            print collection_id
            for index, video in enumerate(video_list):
                try:
                    vid_collection = VideoinCollection(collection_id=collection_id, video_id=video, 
                                                  order=index)
                    vid_collection.save()
                except Exception, e:
                    pass#raise PMANotSaved('For Screening with id: ' + str(screening_id) + ' pma is not getting saved. pma details: '+ str(e))
            print "before bundle"
            return bundle
            
        else:
            pass#raise PMANotSaved('Screening with details: ' + str(bundle.data) + ' can not be saved because attendance list is not available')
    
    
class ActivityResource(BaseResource):
    # page,count -> send order by descding date
    images = fields.ManyToManyField(ImageSpecResource, 'images', null=True, full=True)
    #comments = fields.ToManyField('website.api.CommentResource', 'comment_activity')
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True)
    farmer = fields.ForeignKey(PersonResource, 'farmer', null=True)
    video = fields.ForeignKey(VideoResource, 'video', null=True)
    collection = fields.ForeignKey(CollectionResource, 'collection', null=True, full=True)
    
    def dehydrate_avatarURL (self, bundle):
        if bundle.obj.partner:
            return bundle.obj.partner.logoURL.url
        return bundle.obj.avatarURL

    def dehydrate_date(self, bundle):
        return bundle.obj.date.strftime('%b %d, %Y')

    class Meta:
        queryset = Activity.objects.all().order_by('-date')
        resource_name = 'activity'
        filtering={
                   'farmer':ALL_WITH_RELATIONS,
                   'partner':ALL_WITH_RELATIONS,
                   'newsFeed':'exact',
                   }




class UserResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user'

class VideoLikeResource(ModelResource):
    video = fields.ForeignKey(VideoResource, 'video')
    user = fields.ForeignKey(UserResource, 'user')
    hydrate_video = partial(dict_to_foreign_uri, field_name='video', resource_name='video')
    hydrate_user = partial(dict_to_foreign_uri, field_name='user', resource_name='user')
    class Meta:
        always_return_data = True
        queryset = VideoLike.objects.all()
        resource_name = 'updateVideoLike'
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
                   'video':ALL_WITH_RELATIONS,
                   'user' :ALL_WITH_RELATIONS
                   }

class CommentResource(BaseResource):
    person = fields.ForeignKey(PersonResource, 'person',full=True, null=True)
    video = fields.ForeignKey(VideoResource, 'video', null=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, full=True)
    hydrate_video = partial(dict_to_foreign_uri, field_name='video', resource_name='video')
    hydrate_user = partial(dict_to_foreign_uri, field_name='user', resource_name='user')
    user_imageURL = fields.CharField()
    
    def dehydrate_user_imageURL(self, bundle):
        if bundle.obj.user:
            try :
                provider = bundle.obj.user.social_auth.all()[0].provider
            except Exception, ex:
                return None
            if provider == 'google-oauth2':
                url =  'https://plus.google.com/s2/photos/profile/%s?sz=75' % bundle.obj.user.social_auth.all()[0].extra_data['id']
            elif provider == 'facebook':
                url = 'https://graph.facebook.com/%s/picture?type=large' % bundle.obj.user.social_auth.all()[0].uid
            return url
     
    def hydrate_isOnline(self, bundle):
        bundle.data['isOnline'] = True
        return bundle
    
    #===========================================================================
    # inReplyToCommentUID = fields.ForeignKey('website.api.CommentResource', 'inReplyToCommentUID', null=True)
    # in videoID out Comment
    # in activityID out Comment
    #===========================================================================
    class Meta:
        always_return_data = True
        queryset = Comment.objects.order_by('-date', '-uid').all()
        resource_name = 'comment'
        authentication = Authentication()
        authorization = Authorization()
        filtering={
                   'video':ALL_WITH_RELATIONS,
                   'text':ALL,
                   'user':ALL_WITH_RELATIONS,
                   }