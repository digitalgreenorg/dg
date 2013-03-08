from django.db import models
from django.contrib.auth.models import User
from website.user_models import CommentLike, TimeWatched, VideoLike, UserCollectionHistory

# Create your models here.
class Country(models.Model):
    countryCode = models.CharField(max_length=20,primary_key = True)
    countryName = models.CharField(max_length=100)

class Interest(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=500)

class Farmer(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    thumbnailURL = models.CharField(max_length=100, blank=True)
    imageURL = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    #groups =
    interests = models.ManyToManyField(Interest,related_name='farmer_interests')
    
    def update(self, name=None, thumbnailURL=None, imageURL=None, village=None, block= None,district= None, state = None, country= None):
        self.name = name
        self.thumbnailURL = thumbnailURL
        self.imageURL = imageURL
        self.village = village
        self.block = block
        self.district = district
        self.state = state
        self.country = country
        print "saving"
        self.save()
        print "exiting"
           

    
class Partner(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    joinDate = models.DateField()
    logoURL = models.URLField(max_length=200, blank=True)
    collectionCount = models.BigIntegerField(null=True, blank=True)
    #badges=
    farmers=models.ManyToManyField(Farmer,related_name='farmer_partner')
    def update(self,uid=None, name=None, description=None, location=None, joindate=None, logoURL=None, collectionCount=None, farmers=None):
        if not farmers == None:
            self.farmers.add(farmers)
        
        
    
class Language(models.Model):
    languageCode = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    
class Video(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    title = models.CharField(max_length=100)
    thumbnailURL = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    youtubeID = models.CharField(max_length=20)
    duration = models.BigIntegerField(null=True, blank=True)
    date = models.DateField()
    onlineLikes = models.BigIntegerField(null=True, blank=True)
    offlineLikes = models.BigIntegerField(null=True, blank=True)
    onlineViews = models.BigIntegerField(null=True, blank=True)
    offlineViews = models.BigIntegerField(null=True, blank=True)
    adoptions = models.BigIntegerField(null=True, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=500, blank=True)
    subsector = models.CharField(max_length=500, blank=True)
    topic = models.CharField(max_length=500, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    partnerUID = models.ForeignKey(Partner,related_name='partner_videos')
    language = models.ForeignKey(Language,max_length=20, related_name='language_videos')
    
        
class Collection(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    title = models.CharField(max_length=500)
    thumbnailURL = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100)
    country = models.ForeignKey(Country,related_name='related_collections')
    partnerUID = models.ForeignKey(Partner,related_name='partner_collections')
    language = models.ForeignKey(Language,max_length=20, related_name='language_collections')
    videos = models.ManyToManyField(Video,related_name='video_collections')
    tags = models.CharField(max_length=500, blank=True)
    sector = models.CharField(max_length=500, blank=True)
    subsector = models.CharField(max_length=500, blank=True)
    topic = models.CharField(max_length=500, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    
class ImageSpec(models.Model):
    imageURL = models.URLField(max_length=200) 
    #allStrings
    #imageLinkURLs
    
class Activity(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    date = models.DateField()
    type = models.CharField(max_length=20,choices = (('F','Farmer'),('P','Partner')) )
    title = models.CharField(max_length=100)
    textContent = models.TextField()
    avatarURL = models.CharField(max_length=100, blank=True)
    youtubeVideoID = models.CharField(max_length=20,blank=True)
    images = models.ManyToManyField(ImageSpec)
    
class Person(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    avatarURL = models.URLField(max_length=200, blank=True)
    facebookID = models.CharField(max_length=50, blank=True)
    twitterID = models.CharField(max_length=50, blank=True) 
    youtubeID = models.CharField(max_length=50, blank=True) 
    linkedInID =  models.CharField(max_length=50, blank=True)
    authToken = models.CharField(max_length=20, blank=True)
    
class Comment(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    date = models.DateField()
    text = models.TextField()
    isOnline = models.BooleanField()
    partnerUID = models.ForeignKey(Partner,related_name='partner_comments',null= True, blank=True)
    personUID = models.ForeignKey(Person,related_name='person_comments',null= True, blank=True)
    inReplyToCommentUID= models.ForeignKey('self',related_name='replies',null= True, blank=True)
    videoUID = models.ForeignKey(Video,related_name='video_comments',null= True, blank=True)
    farmerUID = models.ForeignKey(Farmer,related_name='farmer_comments',null= True, blank=True)
    
class FilterValueDescription(models.Model):
    value = models.CharField(max_length=100)
    itemCount = models.BigIntegerField()
    
class SearchCompletion(models.Model):
    type = models.CharField(max_length=10,choices = (('T','Topic'),('V','Videos'),('P','Partners')))
    searchTerm = models.CharField(max_length=100)
    
class VideoWatchRecord(models.Model): 
    videoUID = models.ForeignKey(Video,related_name='video_watchrecord')
    personUID = models.ForeignKey(Person,related_name='person_watchrecord')
    timeWatched = models.BigIntegerField()
    
class User(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    authToken = models.CharField(max_length=100, blank=True)
    avatarURL = models.URLField(max_length=200, blank=True)
    facebookID = models.CharField(max_length=50, blank=True)
    twitterID = models.CharField(max_length=50, blank=True) 
    youtubeID = models.CharField(max_length=50, blank=True) 
    linkedInID =  models.CharField(max_length=50, blank=True)
    authToken = models.CharField(max_length=20, blank=True)
 
    
    