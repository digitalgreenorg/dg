from tastypie.resources import ModelResource
from tastypie import fields
from website.models import Video, Language, Country, Farmer, Activity, Collection, Partner, Interest, Comment


class BaseResource(ModelResource):
    class Meta:
        resource_name = 'base'
    def dehydrate(self, bundle):
        bundle.data['objectType'] = self.Meta.resource_name
        return bundle

class CountryResource(BaseResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'


class LanguageResource(BaseResource):
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'

class InterestResource(BaseResource):
    class Meta:
        queryset = Interest.objects.all()
        resource_name = 'interest'

               
class FarmerResource(BaseResource):
    interest = fields.ManyToManyField(InterestResource, 'interests',full=True)
    class Meta:
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
                
class PartnerResource(BaseResource):
    farmers= fields.ManyToManyField(FarmerResource, 'farmers')
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'

class VideoResource(BaseResource):
    partner = fields.ForeignKey(PartnerResource, 'partnerUID',full=True)
    language = fields.ForeignKey(LanguageResource, 'language',full=True)
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
 
class CollectionResource(BaseResource):
    country = fields.ForeignKey(CountryResource, 'country',full=True)
    videos = fields.ManyToManyField(VideoResource, 'videos')
    partner = fields.ForeignKey(PartnerResource, 'partnerUID')
    language = fields.ForeignKey(LanguageResource, 'language',full=True)
    class Meta:
        queryset = Collection.objects.all()
        resource_name = 'collection'

class ActivityResource(BaseResource):
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activity'

class CommentResource(BaseResource):
    farmer = fields.ForeignKey(FarmerResource, 'farmerUID',full=True, null=True)
    video = fields.ForeignKey(VideoResource, 'videoUID', null=True)
    partner = fields.ForeignKey(PartnerResource, 'partnerUID',full=True,null=True)
    person = fields.ForeignKey(LanguageResource, 'personUID',full=True, null=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
