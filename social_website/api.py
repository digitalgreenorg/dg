from tastypie.resources import ModelResource
from tastypie import fields
from social_website.models import Video, Language, Country, Farmer, Activity, Collection, Partner, Interests, Comment, ImageSpec
from functools import partial
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from django.http import HttpResponse


def many_to_many_to_subfield(bundle, field_name, sub_field_names):
    sub_fields = getattr(bundle.obj, field_name).values_list(*sub_field_names,flat=True)
    return sub_fields

def many_to_many_to_subfield_rev(bundle, field_name, sub_field_names):
    print bundle.data
    sub_fields = getattr(bundle.data, field_name).values_list(*sub_field_names,flat=True)
    return sub_fields

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

class CountryResource(BaseResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        
class InterestsResource(BaseResource):
    class Meta:
        queryset = Interests.objects.all()
        resource_name = 'interests'

class ImageSpecResource(BaseResource):
    class Meta:
        queryset = ImageSpec.objects.all()
        resource_name = 'imagespec'

class LanguageResource(BaseResource):
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'
        include_resource_uri = False
        filtering={
                   'name':ALL
                   }
        
class PartnerResource(BaseResource):
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'
        excludes = ['videos', 'likes', 'views', 'adoptions', 'badges']

class FarmerResource(BaseResource):
    interests = fields.ManyToManyField(InterestsResource, 'interests', null=True)
    dehydrate_interests = partial(many_to_many_to_subfield, field_name='interests',sub_field_names=['name'])
    partner = fields.ForeignKey(PartnerResource, 'partner',full=True, null=True)
    # M2M collections
    class Meta:
        queryset = Farmer.objects.all()
        resource_name = 'farmer'

class PartnerFarmerResource(BaseResource):
    farmer = fields.ToManyField('social_website.api.FarmerResource', 'farmer_set',full=True)
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partnerFarmers'
        fields=['farmer','name','uid']
        filtering={
                   'uid':ALL
                   }


class VideoResource(BaseResource):
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
        excludes = ['sector','subsector','topic','subtopic','subject','state']
    def dehydrate(self, bundle):
        bundle.data['tags'] = Video.objects.get(uid=bundle.data.get('uid')).sector+";"+Video.objects.get(uid=bundle.data.get('uid')).subsector+";"+Video.objects.get(uid=bundle.data.get('uid')).topic+";"+Video.objects.get(uid=bundle.data.get('uid')).subtopic+";"+Video.objects.get(uid=bundle.data.get('uid')).subject 
        return bundle
 
class CollectionResource(BaseCorsResource):
    country = fields.ForeignKey(CountryResource, 'country',full=True)
    videos = fields.ManyToManyField(VideoResource, 'videos',full=True)
    partner = fields.ForeignKey(PartnerResource, 'partner', full=True)
    language = fields.ForeignKey(LanguageResource, 'language',full=True)
    class Meta:
        queryset = Collection.objects.all()
        resource_name = 'collectionsSearch'
        excludes = ['category','subcategory','topic','subtopic','subject']
        filtering={
                   'language':ALL_WITH_RELATIONS
                   }
        ordering={'likes','views','adoptions'}
        
    
class ActivityResource(BaseResource):
    # page,count -> send order by descding date
    images = fields.ManyToManyField(ImageSpecResource, 'images', null=True)
    comments = fields.ToManyField('website.api.CommentResource', 'comment_activity')
    partner = fields.ForeignKey(PartnerResource,'partner',null=True)
    farmer = fields.ForeignKey(FarmerResource,'farmer',null=True)
    user = fields.ForeignKey('website.user_api.UserResource','user',null=True)
    video = fields.ForeignKey(VideoResource,'video',null=True)
    collection = fields.ForeignKey(CollectionResource,'collection',null=True)
    #dehydrate_comments = partial(many_to_many_to_subfield_rev,field_name= 'comments', sub_field_names=['avatarURL','text','inReplyToCommentUID'])
    #dehydrate comments[], imagespec
    # in-> partner famrer user out -> activities total count
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activity'
        filtering={
                   'user':ALL_WITH_RELATIONS,
                   'farmer':ALL_WITH_RELATIONS,
                   'partner':ALL_WITH_RELATIONS
                   }


class CommentResource(BaseResource):
    farmer = fields.ForeignKey(FarmerResource, 'farmerUID',full=True, null=True)
    video = fields.ForeignKey(VideoResource, 'videoUID', null=True)
    user = fields.ForeignKey('website.user_api.UserResource','user',null=True)
    activityURI = fields.ForeignKey(ActivityResource, 'activityURI', null=True)
    inReplyToCommentUID = fields.ForeignKey('website.api.CommentResource', 'inReplyToCommentUID', null=True)
    #in videoID out Comment
    #in activityID out Comment
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        filtering={
                   'video':ALL_WITH_RELATIONS,
                   'activityURI':ALL_WITH_RELATIONS,
                   }
