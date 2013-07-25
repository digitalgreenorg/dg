from django.db import models
from django.core.urlresolvers import reverse
#===============================================================================
# Linked to COCO
#===============================================================================
class Partner(models.Model):
    uid = models.AutoField(primary_key=True)
    coco_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    joinDate = models.DateField()
    logoURL = models.ImageField(upload_to='partner')
    websiteURL = models.URLField(max_length=100, blank=True)
    collection_count = models.PositiveIntegerField(default=0)
    video_count = models.PositiveIntegerField(default=0)
    views = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    adoptions = models.BigIntegerField(default=0)
    def get_absolute_url(self):
        return reverse('social_website.views.partner_view', args=[str(self.name)])
    
class Video(models.Model):
    uid = models.AutoField(primary_key=True)
    coco_id = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    thumbnailURL = models.URLField(max_length=200)
    thumbnailURL16by9 = models.URLField(max_length=200)
    description = models.TextField(blank=True)
    youtubeID = models.CharField(max_length=20)
    duration = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    onlineLikes = models.IntegerField(default=0)
    offlineLikes = models.IntegerField(default=0)
    onlineViews = models.IntegerField(default=0)
    offlineViews = models.IntegerField(default=0)
    adoptions = models.IntegerField(default=0)
    category = models.CharField(max_length=500, blank=True)
    subcategory = models.CharField(max_length=500, blank=True)
    topic = models.CharField(max_length=500, blank=True)
    subtopic = models.CharField(max_length=500, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    partner = models.ForeignKey(Partner)
    language = models.CharField(max_length=20)
    state = models.CharField(max_length=50)

class Person(models.Model):
    uid = models.AutoField(primary_key=True)
    coco_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    thumbnailURL = models.URLField(max_length=100)
    partner = models.ForeignKey(Partner)

#===============================================================================
# Updated from COCO
#===============================================================================
class PersonVideoRecord(models.Model):
    uid = models.AutoField(primary_key=True)
    personID = models.CharField(max_length=20)
    videoID = models.CharField(max_length=20)
    views = models.PositiveSmallIntegerField(default = 0)
    like = models.BooleanField(default=False)
    adopted = models.PositiveSmallIntegerField(default = 0)
    
class Comment(models.Model):
    uid = models.AutoField(primary_key=True)
    date = models.DateField()
    text = models.TextField()
    isOnline = models.BooleanField()
    video = models.ForeignKey(Video)
    person = models.ForeignKey(Person)

#===============================================================================
# Website Models
#===============================================================================
class Collection(models.Model):
    uid = models.AutoField(primary_key = True)
    title = models.CharField(max_length=500)
    thumbnailURL = models.URLField(max_length=200)
    state = models.CharField(max_length=100)
    partner = models.ForeignKey(Partner) #,related_name='partner_collections')
    language = models.CharField(max_length=20)
    videos = models.ManyToManyField(Video) #,related_name='video_collections')
    category = models.CharField(max_length=500, blank=True)
    subcategory = models.CharField(max_length=500, blank=True)
    topic = models.CharField(max_length=500, blank=True)
    subtopic = models.CharField(max_length=500, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    adoptions = models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse('social_website.views.collection_view', 
                       args=[str(self.partner.name), str(self.state), str(self.language), str(self.title)])
    def get_absolute_url_for_video(self, video_index = 1):
        return reverse('social_website.views.collection_view', 
                       args=[str(self.partner.name), str(self.state), str(self.language), str(self.title), str(video_index)])

class FeaturedCollection(models.Model):
    uid = models.AutoField(primary_key=True)
    collection = models.ForeignKey(Collection)
    collageURL = models.URLField(max_length=200)

class ImageSpec(models.Model):
    imageURL = models.URLField(max_length=400) 
    altString = models.CharField(max_length=200)
    imageLinkURL = models.URLField(max_length=400)

class Activity(models.Model):
    uid = models.AutoField(primary_key=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    textContent = models.TextField()
    facebookID = models.CharField(max_length=50, null=True, blank=True)
    avatarURL = models.URLField(max_length=200)
    images = models.ManyToManyField(ImageSpec, null=True, blank=True)
    partner = models.ForeignKey(Partner, null=True, blank=True)
    farmer = models.ForeignKey(Person, null=True, blank=True)
    collection = models.ForeignKey(Collection, null=True, blank=True)
    video = models.ForeignKey(Video, null=True, blank=True)
    newsFeed = models.BooleanField()
    type = models.PositiveSmallIntegerField()
    titleURL = models.URLField(max_length=400)

class Milestone(models.Model):
    uid = models.AutoField(primary_key=True)
    partner = models.ForeignKey(Partner, unique=True)
    videoNumber = models.IntegerField()
    villageNumber = models.IntegerField()
    screeningNumber = models.IntegerField()
    viewerNumber = models.IntegerField()
