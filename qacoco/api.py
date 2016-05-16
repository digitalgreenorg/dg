from datetime import datetime, timedelta
from functools import partial
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict, ModelChoiceField
from tastypie import fields
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource, NOT_AVAILABLE
from tastypie.validation import FormValidation

from qacoco.models import QACocoUser, VideoContentApproval, QAReviewer, VideoQualityReview, DisseminationQuality, AdoptionVerification
from geographies.models import Block, Village, State,District
from dashboard.forms import CategoryForm, SubCategoryForm, VideoForm
from videos.models import Video, Category, SubCategory, NonNegotiable
from qacoco.forms import VideoContentApprovalForm, VideoQualityReviewForm, DisseminationQualityForm, AdoptionVerificationForm,NonNegotiableForm
from people.models import Animator, Person, PersonGroup
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
            form = self.form_class(data, instance = bundle.obj.__class__.objects.get(pk=bundle.data['id']))
        else:
            form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors

def many_to_many_to_subfield(bundle, field_name, sub_field_names):
    sub_fields = getattr(bundle.obj, field_name).values(*sub_field_names)
    return list(sub_fields)

def foreign_key_to_id(bundle, field_name,sub_field_names):
    field = getattr(bundle.obj, field_name)
    if(field == None):
        dict = {}
        for sub_field in sub_field_names:
            dict[sub_field] = None 
    else:
        dict = model_to_dict(field, fields=sub_field_names, exclude=[])
    return dict

def dict_to_foreign_uri(bundle, field_name, resource_name=None):
    field_dict = bundle.data.get(field_name)
    if field_dict.get('id'):
        bundle.data[field_name] = "/qa/api/v1/%s/%s/"%(resource_name if resource_name else field_name, 
                                                    str(field_dict.get('id')))
    else:
        bundle.data[field_name] = None
    return bundle

def get_user_partner_id(user_id):
    if user_id:
        try:
            partner_id = QACocoUser.objects.get(user_id = user_id).partner.id
        except Exception as e:
            partner_id = None
            raise PartnerDoesNotExist('partner does not exist for user '+ user_id+" : "+ e)
        
    return partner_id

def get_user_videos(user_id):
    ###Videos produced by partner with in the same state
    qacoco_user = QACocoUser.objects.get(user_id = user_id)
    districts = qacoco_user.get_districts()
    user_states = State.objects.filter(district__in = districts).distinct().values_list('id', flat=True)
    ###FIRST GET VIDEOS PRODUCED IN STATE WITH SAME PARTNER
    videos = Video.objects.filter(village__block__district__state__in = user_states, partner_id = qacoco_user.partner_id).values_list('id', flat = True)
    return (list(videos))

def get_user_non_negotiable(user_id):
    video_list = get_user_videos(user_id)
    return list(NonNegotiable.objects.filter(video_id__in = video_list).values_list('id', flat = True))

class DistrictAuthorization(Authorization):
    def __init__(self, field):
        self.filter_keyword = field
    
    def read_list(self, object_list, bundle):
        districts = QACocoUser.objects.get(user_id= bundle.request.user.id).get_districts()
        kwargs = {}
        kwargs[self.filter_keyword] = districts
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.filter_keyword] = QACocoUser.objects.get(user_id= bundle.request.user.id).get_districts()
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound( "Not allowed to download District" )

class VideoAuthorization(Authorization):
    def read_list(self, object_list, bundle):        
        return object_list.filter(id__in= get_user_videos(bundle.request.user.id))
    
    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_videos(bundle.request.user.id):
            return True
        else:
            raise NotFound( "Not allowed to download video")

class NonNegotiableAuthorization(Authorization):
    def read_list(self, object_list, bundle):        
        return object_list.filter(id__in= get_user_non_negotiable(bundle.request.user.id))
    
    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_non_negotiable(bundle.request.user.id):
            return True
        else:
            raise NotFound( "Not allowed to download Non-Negotiable")


class BaseResource(ModelResource):
    
    def full_hydrate(self, bundle):
        bundle = super(BaseResource, self).full_hydrate(bundle)
        bundle.obj.user_modified_id = bundle.request.user.id
        return bundle
    
    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        self.authorized_create_detail(self.get_object_list(bundle.request), bundle)
        bundle = self.full_hydrate(bundle)
        bundle.obj.user_created_id = bundle.request.user.id
        return self.save(bundle)

class QAReviewerResource(ModelResource):    
    class Meta:
        max_limit = None
        queryset = QAReviewer.objects.all()
        resource_name = 'qareviewer'
        authentication = SessionAuthentication()
        authorization = Authorization()

class VideoResource(BaseResource):
    non_negotiables = fields.ListField()
    class Meta:
        max_limit = None 
        queryset = Video.objects.all()
        resource_name = 'video'
        authentication = SessionAuthentication()
        authorization = Authorization()

class MediatorResource(BaseResource):
    class Meta:
                max_limit = None
                queryset = Animator.objects.all()
                resource_name = 'mediator'
                authentication = Authentication()
                authorization = DistrictAuthorization('district_id__in')

class BlockResource(BaseResource):
    class Meta:
                
                max_limit = None
                queryset = Block.objects.all()
                resource_name = 'block'
                authentication = SessionAuthentication()
                authorization = DistrictAuthorization('district_id__in')

class VillageResource(BaseResource):
    class Meta:
                max_limit = None
                queryset = Village.objects.all()
                resource_name = 'village'
                authentication = SessionAuthentication()
                authorization = DistrictAuthorization('block__district_id__in')

class PersonResource(BaseResource):
    class Meta:
                max_limit = None
                queryset = Person.objects.all()
                resource_name = 'person'
                authentication = Authentication()
                authorization = DistrictAuthorization('village__block__district_id__in')

class PersonGroupResource(BaseResource):
    class Meta:
                max_limit = None
                queryset = PersonGroup.objects.all()
                resource_name = 'group'
                authentication = Authentication()
                authorization = DistrictAuthorization('village__block__district_id__in')

class NonNegotiableResource(BaseResource):
    video = fields.ForeignKey(VideoResource, 'video')
    class Meta:
        max_limit = None
        queryset = NonNegotiable.objects.prefetch_related('video').all()
        resource_name = 'nonnegotiable'
        authentication = SessionAuthentication()
        authorization = Authorization()
        validation = ModelFormValidation(form_class=NonNegotiableForm)
        excludes = ['time_created', 'time_modified']
        always_return_data = True
    dehydrate_video = partial(foreign_key_to_id, field_name='video', sub_field_names=['id','title'])
    hydrate_video = partial(dict_to_foreign_uri, field_name='video', resource_name='video')



class VideoContentApprovalResource(BaseResource):
        video = fields.ForeignKey(VideoResource, 'video')
        qareviewer = fields.ForeignKey(QAReviewerResource, 'qareviewer')
        class Meta:
                queryset = VideoContentApproval.objects.all()
                always_return_data = True
                resource_name = 'VideoContentApproval'
                authorization = Authorization()
                authentication = SessionAuthentication()
                validation = ModelFormValidation(form_class=VideoContentApprovalForm)
        dehydrate_video = partial(foreign_key_to_id, field_name = 'video', sub_field_names=['id','title'])
        hydrate_video = partial(dict_to_foreign_uri, field_name ='video')
        dehydrate_qareviewer = partial(foreign_key_to_id, field_name = 'qareviewer', sub_field_names=['id','reviewer_name'])
        hydrate_qareviewer = partial(dict_to_foreign_uri, field_name ='qareviewer')

class VideoQualityReviewResource(BaseResource):
        video = fields.ForeignKey(VideoResource, 'video')
        qareviewer = fields.ForeignKey(QAReviewerResource, 'qareviewer')
        class Meta:
                queryset = VideoQualityReview.objects.all()
                always_return_data = True
                resource_name = 'VideoQualityReview'
                authorization = Authorization()
                authentication = Authentication()
                validation = ModelFormValidation(form_class=VideoQualityReviewForm)
        dehydrate_video = partial(foreign_key_to_id, field_name = 'video', sub_field_names=['id','title'])
        hydrate_video = partial(dict_to_foreign_uri, field_name ='video')
        dehydrate_qareviewer = partial(foreign_key_to_id, field_name = 'qareviewer', sub_field_names=['id','reviewer_name'])
        hydrate_qareviewer = partial(dict_to_foreign_uri, field_name ='qareviewer')

class DisseminationQualityResource(BaseResource):
        block = fields.ForeignKey(BlockResource, 'block')
        village = fields.ForeignKey(VillageResource, 'village')
        mediator = fields.ForeignKey(MediatorResource, 'mediator')
        video = fields.ForeignKey(VideoResource, 'video')
        qareviewer = fields.ForeignKey(QAReviewerResource, 'qareviewer')
        
        class Meta:
                queryset = DisseminationQuality.objects.all()
                always_return_data = True
                resource_name = 'DisseminationQuality'
                authorization = Authorization()
                authentication = Authentication()
                validation = ModelFormValidation(form_class=DisseminationQualityForm)
        dehydrate_video = partial(foreign_key_to_id, field_name = 'video', sub_field_names=['id','title'])
        hydrate_video = partial(dict_to_foreign_uri, field_name ='video')
        
        dehydrate_block = partial(foreign_key_to_id, field_name = 'block', sub_field_names=['id','block_name'])
        hydrate_block = partial(dict_to_foreign_uri, field_name ='block')
        dehydrate_village = partial(foreign_key_to_id, field_name = 'village', sub_field_names=['id','village_name'])
        hydrate_village = partial(dict_to_foreign_uri, field_name ='village')
        dehydrate_mediator = partial(foreign_key_to_id, field_name = 'mediator', sub_field_names=['id','name'])
        hydrate_mediator = partial(dict_to_foreign_uri, field_name ='mediator')
        dehydrate_qareviewer = partial(foreign_key_to_id, field_name = 'qareviewer', sub_field_names=['id','reviewer_name'])
        hydrate_qareviewer = partial(dict_to_foreign_uri, field_name ='qareviewer')

class AdoptionVerificationResource(BaseResource):
        block = fields.ForeignKey(BlockResource, 'block')
        village = fields.ForeignKey(VillageResource, 'village')
        mediator = fields.ForeignKey(MediatorResource, 'mediator')
        video = fields.ForeignKey(VideoResource, 'video')
        person = fields.ForeignKey(PersonResource, 'person')
        group = fields.ForeignKey(PersonGroupResource, 'group')
        qareviewer = fields.ForeignKey(QAReviewerResource, 'qareviewer')
        class Meta:
                queryset = AdoptionVerification.objects.all()
                always_return_data = True
                resource_name = 'AdoptionVerification'
                authorization = Authorization()
                authentication = Authentication()
                validation = ModelFormValidation(form_class=AdoptionVerificationForm)
        dehydrate_video = partial(foreign_key_to_id, field_name = 'video', sub_field_names=['id','title'])
        hydrate_video = partial(dict_to_foreign_uri, field_name ='video')
        dehydrate_block = partial(foreign_key_to_id, field_name = 'block', sub_field_names=['id','block_name'])
        hydrate_block = partial(dict_to_foreign_uri, field_name ='block')
        dehydrate_village = partial(foreign_key_to_id, field_name = 'village', sub_field_names=['id','village_name'])
        hydrate_village = partial(dict_to_foreign_uri, field_name ='village')
        dehydrate_mediator = partial(foreign_key_to_id, field_name = 'mediator', sub_field_names=['id','name'])
        hydrate_mediator = partial(dict_to_foreign_uri, field_name ='mediator')
        dehydrate_group = partial(foreign_key_to_id, field_name = 'group', sub_field_names=['id','group_name'])
        hydrate_group = partial(dict_to_foreign_uri, field_name ='group')
        dehydrate_qareviewer = partial(foreign_key_to_id, field_name = 'qareviewer', sub_field_names=['id','reviewer_name'])
        hydrate_qareviewer = partial(dict_to_foreign_uri, field_name ='qareviewer')
        dehydrate_person = partial(foreign_key_to_id, field_name = 'person', sub_field_names=['id','person_name'])
        hydrate_person = partial(dict_to_foreign_uri, field_name ='person')
