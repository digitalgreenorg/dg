from django.db import models
from django.contrib.auth.models import User
#from website.user_models import CommentLike, TimeWatched, VideoLike, UserCollectionHistory

# Create your models here.
class Country(models.Model):
    countryName = models.CharField(max_length=100)

class Interests(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=500)
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
class Badge(models.Model):
    name = models.CharField(primary_key = True, max_length =20)
    url = models.URLField(max_length=100)

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
    
class Partner(models.Model):
    uid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    joinDate = models.DateField()
    logoURL = models.URLField(max_length=200)
    collectionCount = models.BigIntegerField(null=True, blank=True)
    #Internal Fields
    videos = models.BigIntegerField(null=True, blank=True)
    views = models.BigIntegerField(null=True, blank=True)
    likes = models.BigIntegerField(null=True, blank=True)
    adoptions = models.BigIntegerField(null=True, blank=True)

    
class Language(models.Model):
    name = models.CharField(max_length=100)
    
    
class Video(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    title = models.CharField(max_length=100)
    thumbnailURL = models.URLField(max_length=200)
    description = models.TextField(blank=True)
    youtubeID = models.CharField(max_length=20, )
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    onlineLikes = models.IntegerField(null=True, blank=True)
    offlineLikes = models.IntegerField(null=True, blank=True)
    onlineViews = models.IntegerField(null=True, blank=True)
    offlineViews = models.IntegerField(null=True, blank=True)
    adoptions = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    
    # Internally used fields
    sector = models.CharField(max_length=500, blank=True)
    subsector = models.CharField(max_length=500, blank=True)
    topic = models.CharField(max_length=500, blank=True)
    subtopic = models.CharField(max_length=500, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    partner = models.ForeignKey(Partner,related_name='partner_videos')
    language = models.ForeignKey(Language,max_length=20, related_name='language_videos')
    state = models.CharField(max_length=50)
    
        
class Collection(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    title = models.CharField(max_length=500)
    thumbnailURL = models.URLField(max_length=200)
    state = models.CharField(max_length=100)
    country = models.ForeignKey(Country,related_name='related_collections')
    partner = models.ForeignKey(Partner,related_name='partner_collections')
    language = models.ForeignKey(Language,max_length=20, related_name='language_collections')
    videos = models.ManyToManyField(Video,related_name='video_collections')
    
    # INTERNAL FIELDS
    category = models.CharField(max_length=500, blank=True)
    subcategory = models.CharField(max_length=500, blank=True)
    topic = models.CharField(max_length=500, blank=True)
    subtopic = models.CharField(max_length=500, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    adoptions = models.IntegerField(null=True, blank=True)
    
class Farmer(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    thumbnailURL = models.URLField(max_length=100)
    village = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    interests = models.ManyToManyField(Interests,related_name='farmer_interests',null=True,blank=True)
    partner = models.ForeignKey(Partner)
    
    #    Internal Field
    collections = models.ManyToManyField(Collection,null=True,blank=True)

    
class ImageSpec(models.Model):
    imageURL = models.URLField(max_length=200) 
    altString = models.CharField(max_length=200)
    imageLinkURL = models.URLField(max_length=200)
    
class Activity(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    date = models.DateField()
    textContent = models.TextField()
    avatarURL = models.URLField(max_length=200)
    images = models.ManyToManyField(ImageSpec,null=True,blank=True)
    partner = models.ForeignKey(Partner,null=True,blank=True)
    farmer = models.ForeignKey(Farmer,null=True,blank=True)
    collection = models.ForeignKey(Collection,null=True,blank=True)
    user = models.ForeignKey(User,null=True,blank=True)
    video = models.ForeignKey(Video)
    
class Comment(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    date = models.DateField()
    text = models.TextField()
    isOnline = models.BooleanField()
    user = models.ForeignKey(User,related_name='user_comments',null= True, blank=True)
    inReplyToCommentUID= models.ForeignKey('self',related_name='replies',null= True, blank=True)
    video = models.ForeignKey(Video,related_name='video_comments',null= True, blank=True)
    farmer = models.ForeignKey(Farmer,related_name='farmer_comments',null= True, blank=True)
    activityURI = models.ForeignKey(Activity,related_name='comment_activity',null= True, blank=True)
    
class FilterValueDescription(models.Model):
    value = models.CharField(max_length=200)
    itemCount = models.BigIntegerField()
    
class SearchCompletion(models.Model):
    type = models.CharField(max_length=10,choices = (('T','Topic'),('V','Videos'),('P','Partners')))
    searchTerm = models.CharField(max_length=100)
    targetURL = models.URLField(max_length=200)
    
class VideoWatchRecord(models.Model): 
    videoUID = models.ForeignKey(Video,related_name='video_watchrecord')
    user = models.ForeignKey(User,related_name='user_watchrecord')
    timeWatched = models.BigIntegerField()

    
    
