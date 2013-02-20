from django.db import models

# Create your models here.
class Video(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    title = models.CharField(max_length=100)
    thumbnailURL = models.CharField(max_length=100)
    description = models.CharField(blank=True)
    youtubeID = models.CharField(max_length=20,blank=True)
    duration = models.BigIntegerField(null=True, blank=True)
    date = models.DateField()
    onlineLikes = models.BigIntegerField(null=True, blank=True)
    offlineLikes = models.BigIntegerField(null=True, blank=True)
    onlineViews = models.BigIntegerField(null=True, blank=True)
    offlineViews = models.BigIntegerField(null=True, blank=True)
    adoptions = models.BigIntegerField(null=True, blank=True)
    tags = models.CharField(max_length=100)
    
class Country(models.Model):
    countryCode = models.CharField(max_length=20,primary_key = True)
    countryName = models.CharField(max_length=20)

    
class Farmer(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    thumbnailURL = models.CharField(max_length=100)
    imageURL = models.CharField(max_length=100)
    village = models.CharField(max_length=20)
    block = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.ForeignKey(Country,related_name = 'related_farmers')
    #groups =
    #interests =  

    
class Partner(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    joinDate = models.DateField()
    logoURL = models.URLField(max_length=200)
    collectionCount = models.BigIntegerField(null=True, blank=True)
    #badges=
    farmers=models.ManyToManyField(Farmer,related_name='farmer_partner')
    
    
class Collection(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    title = models.CharField(max_length=100)
    thumbnailURL = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    country = models.ForeignKey(Country,related_name='related_collections')
    partnerUID = models.ForeignKey(Partner,related_name='partner_collections')
    language = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    videos = models.ManyToManyField(Video,related_name='video_collections')
    tags = models.CharField(max_length=100)
    sector = models.CharField(max_length=20,null=True, blank=True)
    subsector = models.CharField(max_length=20,null=True, blank=True)
    topic = models.CharField(max_length=20,null=True, blank=True)
    subject = models.CharField(max_length=20,null=True, blank=True)
    
class ImageSpec(models.Model):
    imageURL = models.URLField(max_length=200) 
    #allStrings
    #imageLinkURLs
    
class Activity(models.Model):
    uid = models.CharField(max_length=20,primary_key = True)
    date = models.DateField()
    #type = models.CharField(max_length=20,choices = ['F','P'] )
    title = models.CharField(max_length=100)
    textContent = models.CharField()
    avatarURL = models.CharField(max_length=100)
    #collectionUID = models.ForeignKey(Collection, related_name='collection_activity', blank=True)
    #youtubeVideoID = models.CharField(max_length=20,blank=True)
    images = models.ManyToManyField(ImageSpec)
    
class Language(models.Model):
    countryCode = models.ForeignKey(Country)
    languageCode = models.CharField(max_length=20,primary_key = True)
    name = models.CharField(max_length=20)
    
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
    
class FilterValueDescription(models.Model):
    value = models.CharField(max_length=100)
    itemCount = models.BigIntegerField()
    
class SearchCompletion(models.Model):
    type = models.CharField(max_length=10,choices = ['Topic','Videos','Partners'])
    searchTerm = models.CharField(max_length=100)
    
class VideoWatchRecord(models.Model): 
    videoUID = models.ForeignKey(Video,related_name='partner_comments')
    personUID = models.ForeignKey(Person,related_name='partner_comments')
    timeWatched = models.BigIntegerField()
    
class UserInfo(models.Model):
    personUID = models.ForeignKey(Person,related_name='partner_comments')
    #authToken
    #name
    avatarURL = models.URLField(max_length=200)
    #facebookID string
    #twitterID string 
    #youtubeID string 
    #linkedInID string

    
