# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        count = 0
        for collection in orm['social_website.Collection'].objects.all():
            videos_collection = collection.videos.all()
            for video in videos_collection:
                if (video.thumbnailURL!=""):
                    collection.thumbnailURL = video.thumbnailURL16by9
                    collection.save()
                    count += 1
                    break
        print ("Number Of Collection Url Updated :"), count

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'social_website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Collection']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Farmer']", 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social_website.ImageSpec']", 'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']", 'null': 'True', 'blank': 'True'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.User']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Video']"})
        },
        'social_website.badge': {
            'Meta': {'object_name': 'Badge'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        },
        'social_website.collection': {
            'Meta': {'object_name': 'Collection'},
            'adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_collections'", 'to': "orm['social_website.Country']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_collections'", 'to': "orm['social_website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_collections'", 'symmetrical': 'False', 'to': "orm['social_website.Video']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'social_website.comment': {
            'Meta': {'object_name': 'Comment'},
            'activityURI': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_activity'", 'null': 'True', 'to': "orm['social_website.Activity']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmer_comments'", 'null': 'True', 'to': "orm['social_website.Farmer']"}),
            'inReplyToCommentUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['social_website.Comment']"}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_comments'", 'null': 'True', 'to': "orm['social_website.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_comments'", 'null': 'True', 'to': "orm['social_website.Video']"})
        },
        'social_website.country': {
            'Meta': {'object_name': 'Country'},
            'countryName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social_website.farmer': {
            'Meta': {'object_name': 'Farmer'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social_website.Collection']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'farmer_interests'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['social_website.Interests']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social_website.filtervaluedescription': {
            'Meta': {'object_name': 'FilterValueDescription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemCount': ('django.db.models.fields.BigIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'social_website.imagespec': {
            'Meta': {'object_name': 'ImageSpec'},
            'altString': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageLinkURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'social_website.interests': {
            'Meta': {'object_name': 'Interests'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'social_website.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social_website.partner': {
            'Meta': {'object_name': 'Partner'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collectionCount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'joinDate': ('django.db.models.fields.DateField', [], {}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'logoURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'social_website.searchcompletion': {
            'Meta': {'object_name': 'SearchCompletion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'searchTerm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'targetURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'social_website.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social_website.user': {
            'Meta': {'object_name': 'User'},
            'authToken': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'linkedInID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitterID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'social_website.video': {
            'Meta': {'object_name': 'Video'},
            'adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'offlineLikes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offlineViews': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineLikes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineViews': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_videos'", 'to': "orm['social_website.Partner']"}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subsector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['social_website.Tag']", 'symmetrical': 'False'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailURL16by9': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailURL4by3': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'social_website.videowatchrecord': {
            'Meta': {'object_name': 'VideoWatchRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeWatched': ('django.db.models.fields.BigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_watchrecord'", 'to': "orm['social_website.User']"}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_watchrecord'", 'to': "orm['social_website.Video']"})
        }
    }

    complete_apps = ['social_website']
    symmetrical = True
