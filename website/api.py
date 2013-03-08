from tastypie.resources import ModelResource
from tastypie import fields
from website.models import Video, Language, Country, Farmer, Activity, Collection, Partner, Interests, Comment


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

class FarmerResource(BaseResource):
    # Dehydrate interest to string[]
    # partner FK
    # M2M collections
    class Meta:
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
                
class PartnerResource(BaseResource):
    #dehydrate badges
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'
        excludes = ['videos', 'likes', 'views', 'adoptions', 'badges']

class PartnerFarmerResource(BaseResource):
    #in Parteruid # out farmers
    class Meta:
        queryset = Partner.objects.all()
        resource_name = 'partner'
        excludes = ['videos', 'likes', 'views', 'adoptions', 'badges']


class VideoResource(BaseResource):
    #dehydrate tags
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
        excludes = ['sector','subsector','topic','subtopic','subject','state']
 
class CollectionResource(BaseResource):
    country = fields.ForeignKey(CountryResource, 'country',full=True)
    videos = fields.ManyToManyField(VideoResource, 'videos')
    partner = fields.ForeignKey(PartnerResource, 'partnerUID')
    language = fields.ForeignKey(LanguageResource, 'language',full=True)
    class Meta:
        queryset = Collection.objects.all()
        resource_name = 'collection'
        excludes = ['category','subcategory','topic','subtopic','subject']

class ActivityResource(BaseResource):
    # page,count -> send order by descding date
    #dehydrate comments[], imagespec
    #foreign key partner, farmer, user, collection, video
    # in-> partner famrer user out -> activities total count
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activity'

class CommentResource(BaseResource):
    farmer = fields.ForeignKey(FarmerResource, 'farmerUID',full=True, null=True)
    video = fields.ForeignKey(VideoResource, 'videoUID', null=True)
    #user = fields.ForeignKey
    #activityURI = fields.ForeignKey(LanguageResource, 'personUID',full=True, null=True)
    #inReplyToCommentUID FK
    #in videoID out Comment
    #in activityID out Comment
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
