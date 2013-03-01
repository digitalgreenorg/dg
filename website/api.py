from tastypie.resources import ModelResource
from tastypie import fields
from website.models import Video, Language, Country, Farmer, Activity, Collection, Partner, Interest, Comment
import urllib2


class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'

class LanguageResource(ModelResource):
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'

class InterestResource(ModelResource):
    class Meta:
        queryset = Interest.objects.all()
        resource_name = 'interest'

               
class FarmerResource(ModelResource):
    interest = fields.ManyToManyField(InterestResource, 'interests',full=True)
    class Meta:
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
                
class PartnerResource(ModelResource):
    farmers= fields.ManyToManyField(FarmerResource, 'farmers')
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'

class VideoResource(ModelResource):
    partner = fields.ForeignKey(PartnerResource, 'partnerUID',full=True)
    language = fields.ForeignKey(LanguageResource, 'language',full=True)
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
 
class CollectionResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country',full=True)
    videos = fields.ManyToManyField(VideoResource, 'videos')
    partner = fields.ForeignKey(PartnerResource, 'partnerUID',full=True)
    language = fields.ForeignKey(LanguageResource, 'language',full=True)
    class Meta:
        queryset = Collection.objects.all()
        resource_name = 'collection'

class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activity'

class CommentResource(ModelResource):
    farmer = fields.ForeignKey(FarmerResource, 'farmerUID',full=True, null=True)
    video = fields.ForeignKey(VideoResource, 'videoUID', null=True)
    partner = fields.ForeignKey(PartnerResource, 'partnerUID',full=True,null=True)
    person = fields.ForeignKey(LanguageResource, 'personUID',full=True, null=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
