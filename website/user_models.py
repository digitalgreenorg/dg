from django.contrib.auth.models import User
from django.db import models
    
class UserCollectionHistory(models.Model):
    userUID = models.ForeignKey(User)
    completed = models.ManyToManyField('Collection', related_name = 'completed')
    recentlyViewed = models.ManyToManyField('Collection', related_name = 'viewed')
    likedCollections = models.ManyToManyField('Collection', related_name = 'liked')
    
class VideoLike(models.Model):
    videoUID = models.ForeignKey('Video')
    userUID = models.ForeignKey(User)
    # not putting liked (boolean field)
    
class CommentLike(models.Model):
    commentUID = models.ForeignKey('Comment')
    userUID = models.ForeignKey(User)
    # not putting liked (boolean field)

class TimeWatched(models.Model):
    videoWatchRecord = models.ForeignKey('VideoWatchRecord')
    
    
    

    