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

from qacoco.models import QACocoUser, QAReviewerCategory, VideoQualityReview, DisseminationQuality, AdoptionVerification, QAReviewerName, AdoptionNonNegotiableVerfication
from geographies.models import Block, Village, State, District
from dashboard.forms import CategoryForm, SubCategoryForm, VideoForm
from videos.models import Video, Category, SubCategory, NonNegotiable
from qacoco.forms import VideoQualityReviewForm, DisseminationQualityForm, AdoptionVerificationForm, NonNegotiableForm
from people.models import Animator, Person, PersonGroup
from activities.models import PersonAdoptPractice


class AdoptionVerificationNotSaved(Exception):
    pass


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
            # Handles edit case
            form = self.form_class(
                data, instance=bundle.obj.__class__.objects.get(pk=bundle.data['id']))
        else:
            form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors


def many_to_many_to_subfield(bundle, field_name, sub_field_names):
    sub_fields = getattr(bundle.obj, field_name).values(*sub_field_names)
    return list(sub_fields)


def foreign_key_to_id(bundle, field_name, sub_field_names):
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
    if field_dict and field_dict.get('id'):
        bundle.data[field_name] = "/qa/api/v1/%s/%s/" % (resource_name if resource_name else field_name,
                                                         str(field_dict.get('id')))
    else:
        bundle.data[field_name] = None
    return bundle


def dict_to_foreign_uri_m2m(bundle, field_name, resource_name):
    m2m_list = bundle.data.get(field_name)
    resource_uri_list = []
    for item in m2m_list:
        try:
            resource_uri_list.append("/qa/api/v1/%s/%s/" %
                                     (resource_name, str(item.get('id'))))
        except:
            return bundle
    bundle.data[field_name] = resource_uri_list
    return bundle


def get_user_partner_id(user_id):
    if user_id:
        try:
            partner_id = QACocoUser.objects.get(user_id=user_id).partner.id
        except Exception as e:
            partner_id = None
            raise PartnerDoesNotExist(
                'partner does not exist for user ' + user_id+" : " + e)

    return partner_id


def get_user_videos(user_id):
    # Videos produced with in the same state
    qacoco_user = QACocoUser.objects.get(user_id=user_id)
    blocks = qacoco_user.get_blocks()
    user_states = State.objects.filter(
        district__block__in=blocks).distinct().values_list('id', flat=True)
    user_videos = qacoco_user.get_videos().values_list('id', flat=True)
    videos = Video.objects.filter(
        village__block__district__state__in=user_states).values_list('id', flat=True)
    return set(list(videos) + list(user_videos))


def get_user_mediators(user_id):
    qacoco_user = QACocoUser.objects.get(user_id=user_id)
    blocks = qacoco_user.get_blocks()
    partner = get_user_partner_id(user_id)
    user_districts = District.objects.filter(
        block__in=blocks).distinct().values_list('id', flat=True)
    mediators_from_same_district = Animator.objects.filter(
        district__in=user_districts).distinct().values_list('id', flat=True)
    return mediators_from_same_district


def get_user_non_negotiable(user_id):
    video_list = get_user_videos(user_id)
    return list(NonNegotiable.objects.filter(video_id__in=video_list).values_list('id', flat=True))


class MediatorAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(id__in=get_user_mediators(bundle.request.user.id))

    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_mediators(bundle.request.user.id):
            return True
        # Is the requested object owned by the user?
        else:
            raise NotFound("Not allowed to download Mediator")


# Usable in case of QACOCO User data according to district
'''
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
'''


class BlockAuthorization(Authorization):
    def __init__(self, field):
        self.filter_keyword = field

    def read_list(self, object_list, bundle):
        blocks = QACocoUser.objects.get(
            user_id=bundle.request.user.id).get_blocks()
        kwargs = {}
        kwargs[self.filter_keyword] = blocks
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.filter_keyword] = QACocoUser.objects.get(
            user_id=bundle.request.user.id).get_blocks()
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Block")


class BlockVideoAuthorization(Authorization):
    def __init__(self, field):
        self.filter_keyword = field

    def read_list(self, object_list, bundle):
        return object_list.filter(user_created_id=bundle.request.user.id).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        obj = object_list.filter(
            user_created_id=bundle.request.user.id).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Video Quality Review")


class VideoAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(id__in=get_user_videos(bundle.request.user.id))

    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_videos(bundle.request.user.id):
            return True
        else:
            raise NotFound("Not allowed to download video")


class NonNegotiableAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(id__in=get_user_non_negotiable(bundle.request.user.id))

    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_non_negotiable(bundle.request.user.id):
            return True
        else:
            raise NotFound("Not allowed to download Non-Negotiable")


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


class QAReviewerCategoryResource(ModelResource):
    class Meta:
        max_limit = None
        queryset = QAReviewerCategory.objects.all()
        resource_name = 'qareviewercategory'
        authentication = SessionAuthentication()
        authorization = Authorization()


class QAReviewerNameResource(ModelResource):
    class Meta:
        max_limit = None
        queryset = QAReviewerName.objects.all()
        resource_name = 'qareviewername'
        authentication = SessionAuthentication()
        authorization = Authorization()


class VideoResource(BaseResource):
    non_negotiables = fields.ListField()

    class Meta:
        max_limit = None
        queryset = Video.objects.all()
        resource_name = 'video'
        authentication = SessionAuthentication()
        authorization = VideoAuthorization()


class BlockResource(BaseResource):
    class Meta:
        max_limit = None
        queryset = Block.objects.all()
        resource_name = 'block'
        authentication = SessionAuthentication()
        authorization = BlockAuthorization('id__in')


class VillageResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block')

    class Meta:
        max_limit = None
        queryset = Village.objects.all()
        resource_name = 'village'
        authentication = SessionAuthentication()
        authorization = BlockAuthorization('block_id__in')
    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id', 'block_name'])
    hydrate_block = partial(dict_to_foreign_uri,
                            field_name='block', resource_name='block')


class MediatorResource(BaseResource):
    assigned_villages = fields.ListField()

    class Meta:
        max_limit = None
        queryset = Animator.objects.all()
        #queryset = Animator.objects.prefetch_related('assigned_villages', 'district', 'partner').all()
        resource_name = 'mediator'
        authentication = Authentication()
        authorization = MediatorAuthorization()
    hydrate_assigned_villages = partial(
        dict_to_foreign_uri_m2m, field_name='assigned_villages', resource_name='village')

    def dehydrate_assigned_villages(self, bundle):
        return [{'id': vil.id, 'village_name': vil.village_name} for vil in set(bundle.obj.assigned_villages.all())]

    def dehydrate_mediator_label(self, bundle):
        # for sending out label incase of dropdowns
        return ','.join([vil.village_name for vil in set(bundle.obj.assigned_villages.all())])


class PersonGroupResource(BaseResource):
    village = fields.ForeignKey(VillageResource, 'village')

    class Meta:
        max_limit = None
        queryset = PersonGroup.objects.all()
        resource_name = 'group'
        authentication = Authentication()
        authorization = BlockAuthorization('village__block_id__in')
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])
    hydrate_village = partial(
        dict_to_foreign_uri, field_name='village', resource_name='village')


class PersonResource(BaseResource):
    village = fields.ForeignKey(VillageResource, 'village')
    group = fields.ForeignKey(PersonGroupResource, 'group', null=True)

    class Meta:
        max_limit = None
        person_id = PersonAdoptPractice.objects.filter(date_of_adoption__gte=datetime.now(
        ).date() - timedelta(days=365)).values_list('person', flat=True)
        queryset = Person.objects.filter(id__in=person_id)
        resource_name = 'person'
        authentication = Authentication()
        authorization = BlockAuthorization('village__block_id__in')
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])
    dehydrate_group = partial(
        foreign_key_to_id, field_name='group', sub_field_names=['id', 'group_name'])
    hydrate_village = partial(
        dict_to_foreign_uri, field_name='village', resource_name='village')
    hydrate_group = partial(dict_to_foreign_uri,
                            field_name='group', resource_name='group')


class NonNegotiableResource(BaseResource):
    video = fields.ForeignKey(VideoResource, 'video')

    class Meta:
        max_limit = None
        queryset = NonNegotiable.objects.prefetch_related('video').all()
        resource_name = 'nonnegotiable'
        authentication = SessionAuthentication()
        authorization = NonNegotiableAuthorization()
        validation = ModelFormValidation(form_class=NonNegotiableForm)
        excludes = ['time_created', 'time_modified']
        always_return_data = True
    dehydrate_video = partial(
        foreign_key_to_id, field_name='video', sub_field_names=['id', 'title'])
    hydrate_video = partial(dict_to_foreign_uri,
                            field_name='video', resource_name='video')


class VideoQualityReviewResource(BaseResource):
    video = fields.ForeignKey(VideoResource, 'video')
    qareviewername = fields.ForeignKey(
        QAReviewerNameResource, 'qareviewername')

    class Meta:
        queryset = VideoQualityReview.objects.all()
        always_return_data = True
        resource_name = 'VideoQualityReview'
        authorization = BlockVideoAuthorization('video__in')
        authentication = Authentication()
        validation = ModelFormValidation(form_class=VideoQualityReviewForm)
    dehydrate_video = partial(
        foreign_key_to_id, field_name='video', sub_field_names=['id', 'title'])
    hydrate_video = partial(dict_to_foreign_uri, field_name='video')
    dehydrate_qareviewername = partial(
        foreign_key_to_id, field_name='qareviewername', sub_field_names=['id', 'name'])
    hydrate_qareviewername = partial(
        dict_to_foreign_uri, field_name='qareviewername')


class DisseminationQualityResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block')
    village = fields.ForeignKey(VillageResource, 'village')
    group = fields.ForeignKey(PersonGroupResource, 'group', null=True)
    mediator = fields.ForeignKey(MediatorResource, 'mediator')
    video = fields.ForeignKey(VideoResource, 'video', null=True, blank=True)
    videoes_screened = fields.ToManyField('coco.api.VideoResource', 'videoes_screened', related_name='dissemination_observations')
    qareviewername = fields.ForeignKey(QAReviewerNameResource, 'qareviewername')

    class Meta:
        queryset = DisseminationQuality.objects.all()
        always_return_data = True
        resource_name = 'DisseminationQuality'
        authorization = BlockAuthorization('block_id__in')
        authentication = Authentication()
        validation = ModelFormValidation(form_class=DisseminationQualityForm)

    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id', 'block_name'])
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])
    dehydrate_group = partial(
        foreign_key_to_id, field_name='group', sub_field_names=['id', 'group_name'])
    dehydrate_mediator = partial(
        foreign_key_to_id, field_name='mediator', sub_field_names=['id', 'name'])
    dehydrate_video = partial(
        foreign_key_to_id, field_name='video', sub_field_names=['id', 'title'])
    def dehydrate_videoes_screened(self, bundle):
        return [{'id': video.id, 'title': video.title, } for video in bundle.obj.videoes_screened.all()]

    dehydrate_qareviewername = partial(
        foreign_key_to_id, field_name='qareviewername', sub_field_names=['id', 'name'])
    hydrate_block = partial(dict_to_foreign_uri, field_name='block')
    hydrate_village = partial(
        dict_to_foreign_uri, field_name='village', resource_name='village')
    hydrate_group = partial(dict_to_foreign_uri,
                            field_name='group', resource_name='group')
    hydrate_mediator = partial(
        dict_to_foreign_uri, field_name='mediator', resource_name='mediator')
    hydrate_video = partial(dict_to_foreign_uri, field_name='video', resource_name='video')
    hydrate_videoes_screened = partial(dict_to_foreign_uri_m2m, field_name='videoes_screened', resource_name='video')
    hydrate_qareviewername = partial(dict_to_foreign_uri, field_name='qareviewername')


class AdoptionVerificationResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block')
    village = fields.ForeignKey(VillageResource, 'village')
    mediator = fields.ForeignKey(MediatorResource, 'mediator')
    video = fields.ForeignKey(VideoResource, 'video')
    person = fields.ForeignKey(PersonResource, 'person')
    group = fields.ForeignKey(PersonGroupResource, 'group')
    qareviewername = fields.ForeignKey(
        QAReviewerNameResource, 'qareviewername')
    nonnegotiable = fields.ListField()

    class Meta:
        queryset = AdoptionVerification.objects.all()
        always_return_data = True
        resource_name = 'AdoptionVerification'
        authorization = BlockAuthorization('block_id__in')
        authentication = Authentication()
        validation = ModelFormValidation(form_class=AdoptionVerificationForm)

    def obj_create(self, bundle, **kwargs):
        nonnego_list = bundle.data.get('nonnegotiable')
        if nonnego_list:
            bundle = super(AdoptionVerificationResource,
                           self).obj_create(bundle, **kwargs)
            user_id = None
            if bundle.request.user:
                user_id = bundle.request.user.id
            adoptionverification_id = getattr(bundle.obj, 'id')
            for pma in nonnego_list:
                try:
                    attendance = AdoptionNonNegotiableVerfication(adoptionverification_id=adoptionverification_id, nonnegotiable_id=pma['nonnegotiable_id'], adopted=pma['adopted'],
                                                                  user_created_id=user_id)
                    attendance.save()
                except Exception, e:
                    raise AdoptionVerificationNotSaved('For AdoptionVerification with id: ' + str(
                        adoptionverification_id) + ' pma is not getting saved. pma details: ' + str(e))

            return bundle
        else:
            raise AdoptionVerificationNotSaved(
                'Can not be saved because nonnegotiable list is not available')

    def obj_update(self, bundle, **kwargs):
        # Edit case many to many handling. First clear out the previous related objects and create new objects
        bundle = super(AdoptionVerificationResource,
                       self).obj_update(bundle, **kwargs)
        user_id = None
        if bundle.request.user:
            user_id = bundle.request.user.id

        adoptionverification_id = bundle.data.get('id')
        del_objs = AdoptionNonNegotiableVerfication.objects.filter(
            adoptionverification__id=adoptionverification_id).delete()
        nonnego_list = bundle.data.get('nonnegotiable')
        for pma in nonnego_list:
            pma = AdoptionNonNegotiableVerfication(adoptionverification_id=adoptionverification_id, nonnegotiable_id=pma['nonnegotiable_id'], adopted=pma['adopted'],
                                                   user_created_id=user_id)
            pma.save()
        return bundle

    dehydrate_video = partial(
        foreign_key_to_id, field_name='video', sub_field_names=['id', 'title'])
    hydrate_video = partial(dict_to_foreign_uri, field_name='video')
    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id', 'block_name'])
    hydrate_block = partial(dict_to_foreign_uri, field_name='block')
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])
    hydrate_village = partial(
        dict_to_foreign_uri, field_name='village', resource_name='village')
    dehydrate_mediator = partial(
        foreign_key_to_id, field_name='mediator', sub_field_names=['id', 'name'])
    hydrate_mediator = partial(
        dict_to_foreign_uri, field_name='mediator', resource_name='mediator')
    dehydrate_group = partial(
        foreign_key_to_id, field_name='group', sub_field_names=['id', 'group_name'])
    hydrate_group = partial(dict_to_foreign_uri,
                            field_name='group', resource_name='group')
    dehydrate_qareviewername = partial(
        foreign_key_to_id, field_name='qareviewername', sub_field_names=['id', 'name'])
    hydrate_qareviewername = partial(
        dict_to_foreign_uri, field_name='qareviewername')
    dehydrate_person = partial(
        foreign_key_to_id, field_name='person', sub_field_names=['id', 'person_name'])
    hydrate_person = partial(
        dict_to_foreign_uri, field_name='person', resource_name='person')

    def dehydrate_nonnegotiable(self, bundle):
        return [{'nonnegotiable_id': non.nonnegotiable.id,
                 'nonnegotiable': non.nonnegotiable.non_negotiable,
                 'adopted': non.adopted,
                 }
                for non in bundle.obj.adoptionnonnegotiableverfication_set.all()]
