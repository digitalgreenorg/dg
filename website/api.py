from tastypie.resources import ModelResource
from tastypie import fields
from website.models import Video, Language, Country, Farmer, Activity, Collection, Partner
import urllib2

class VideoResource(ModelResource):
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
 
class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'

class LanguageResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'countryCode',full=True)
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'
               
class FarmerResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country',full=True)
    class Meta:
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
        
class CollectionResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country',full=True)
    videos = fields.ManyToManyField(VideoResource, 'videos')
    class Meta:
        queryset = Collection.objects.all()
        resource_name = 'collection'

        
class ActivityResource(ModelResource):
    collection = fields.ForeignKey(CollectionResource, 'collectionUID',full=True)
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activity'
        #dehydrate_collectionUID=urllib2.urlopen(fields.ForeignKey(CollectionResource, 'collectionUID'))

class PartnerResource(ModelResource):
    farmers= fields.ManyToManyField(FarmerResource, 'farmers')
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'
