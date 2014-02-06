from functools import partial

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import ModelForm
from django.forms.models import model_to_dict, ModelChoiceField

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from social_website.models import Activity, Collection, Comment, ImageSpec, Partner, Person, Video, VideoinCollection, VideoLike
from migration_functions import populate_collection_stats
from post_save_funcs import video_collection_activity


### Reference for below class https://github.com/toastdriven/django-tastypie/issues/152
class ModelFormValidation(FormValidation):
    """
        Override tastypie's standard ``FormValidation`` since this does not care
        about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
        """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]
        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
        # copy data, so we don't modify the bundle
        data = data.copy()
        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])

        # validate and return messages on error
        if request.method == "PUT":
            #Handles edit case
            form = self.form_class(data, instance = bundle.obj.__class__.objects.get(pk=bundle.data['uid']))
        else:
            form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors

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
        allows = ','.join([s.upper() for s in allowed])
 
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


class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        exclude = (['videos', 'likes', 'adoptions', 'views'])


class CollectionResource(BaseCorsResource):
    videos = fields.ListField()
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True)
    hydrate_partner = partial(dict_to_foreign_uri, field_name='partner', resource_name='partner')

    class Meta:
        always_return_data = True
        queryset = Collection.objects.all()
        resource_name = 'collections'
        ordering = {'likes', 'views', 'adoptions'}
        authentication = Authentication()
        authorization = Authorization()
        validation = ModelFormValidation(form_class=CollectionForm)

    def obj_create(self, bundle, **kwargs):
        video_list = bundle.data.get('videos')
        if video_list:
            bundle.data['thumbnailURL'] = Video.objects.get(uid=video_list[0]).thumbnailURL16by9 
            bundle = super(CollectionResource, self).obj_create(bundle, **kwargs)
            collection_id = getattr(bundle.obj,'uid')

            VideoinCollection.objects.filter(collection_id=collection_id).delete()
            for index, video in enumerate(video_list):
                try:
                    vid_collection = VideoinCollection(collection_id=collection_id, video_id=video,
                                                  order=index)
                    vid_collection.save()
                except Exception, e:
                    pass#raise PMANotSaved('For Screening with id: ' + str(screening_id) + ' pma is not getting saved. pma details: '+ str(e))
            Collection_obj = Collection.objects.get(uid=collection_id)
            populate_collection_stats(Collection_obj)
            video_collection_activity(Collection_obj, video_list)
            return bundle
        else:
            pass

    def obj_update(self, bundle, **kwargs):
        #Edit case many to many handling. First clear out the previous related objects and create new objects
        video_list = bundle.data.get('videos')
        if video_list:
            bundle.data['thumbnailURL'] = Video.objects.get(uid=video_list[0]).thumbnailURL16by9 
            bundle = super(CollectionResource, self).obj_update(bundle, **kwargs)
            collection_id = bundle.data.get('uid')

            VideoinCollection.objects.filter(collection_id=collection_id).delete()
            for index, video in enumerate(video_list):
                try:
                    vid_collection = VideoinCollection(collection_id=collection_id, video_id=video,
                                                  order=index)
                    vid_collection.save()
                except Exception, e:
                    pass
            populate_collection_stats(Collection.objects.get(uid=collection_id))
            return bundle

        else:
            pass


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
        queryset = User.objects.all()
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