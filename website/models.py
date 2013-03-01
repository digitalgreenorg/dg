from django.db import models

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
    #type = models.CharField(max_length=20,choices = ['F','P'] )
    title = models.CharField(max_length=100)
    textContent = models.TextField()
    avatarURL = models.CharField(max_length=100, blank=True)
    youtubeVideoID = models.CharField(max_length=20,blank=True)
    images = models.ManyToManyField(ImageSpec)
    
class Person(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    
class Comment(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    date = models.DateField()
    text = models.CharField(max_length=200)
    isOnline = models.BooleanField()
    partnerUID = models.ForeignKey(Partner,related_name='partner_comments')
    personUID = models.ForeignKey(Person,related_name='person_comments')
    inReplyToCommentUID= models.ForeignKey('self',related_name='replies')
    videoUID = models.ForeignKey(Video,related_name='video_comments')
    
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
    
class UserInfo(models.Model):
    personUID = models.ForeignKey(Person,related_name='person_userinfo')
    #authToken
    #name
    avatarURL = models.URLField(max_length=200)
    #facebookID string
    #twitterID string 
    #youtubeID string 
    #linkedInID string

    
