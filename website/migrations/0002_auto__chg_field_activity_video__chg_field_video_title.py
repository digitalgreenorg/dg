# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Activity.video'
        db.alter_column('website_activity', 'video_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Video'], null=True))

        # Changing field 'Video.title'
        db.alter_column('website_video', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'Activity.video'
        db.alter_column('website_activity', 'video_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['website.Video']))

        # Changing field 'Video.title'
        db.alter_column('website_video', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Collection']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Farmer']", 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.ImageSpec']", 'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Partner']", 'null': 'True', 'blank': 'True'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.User']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']", 'null': 'True', 'blank': 'True'})
        },
        'website.badge': {
            'Meta': {'object_name': 'Badge'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        },
        'website.collection': {
            'Meta': {'object_name': 'Collection'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_collections'", 'to': "orm['website.Country']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'language_collections'", 'max_length': '20', 'to': "orm['website.Language']"}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_collections'", 'to': "orm['website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_collections'", 'symmetrical': 'False', 'to': "orm['website.Video']"})
        },
        'website.comment': {
            'Meta': {'object_name': 'Comment'},
            'activityURI': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_activity'", 'null': 'True', 'to': "orm['website.Activity']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmer_comments'", 'null': 'True', 'to': "orm['website.Farmer']"}),
            'inReplyToCommentUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['website.Comment']"}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_comments'", 'null': 'True', 'to': "orm['website.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_comments'", 'null': 'True', 'to': "orm['website.Video']"})
        },
        'website.country': {
            'Meta': {'object_name': 'Country'},
            'countryName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'website.farmer': {
            'Meta': {'object_name': 'Farmer'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.Collection']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'farmer_interests'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['website.Interests']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.filtervaluedescription': {
            'Meta': {'object_name': 'FilterValueDescription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemCount': ('django.db.models.fields.BigIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.imagespec': {
            'Meta': {'object_name': 'ImageSpec'},
            'altString': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageLinkURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'website.interests': {
            'Meta': {'object_name': 'Interests'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.partner': {
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
        'website.searchcompletion': {
            'Meta': {'object_name': 'SearchCompletion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'searchTerm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'targetURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'website.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.user': {
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
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'language_videos'", 'max_length': '20', 'to': "orm['website.Language']"}),
            'offlineLikes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offlineViews': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineLikes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineViews': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_videos'", 'to': "orm['website.Partner']"}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subsector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['website.Tag']", 'symmetrical': 'False'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.videowatchrecord': {
            'Meta': {'object_name': 'VideoWatchRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeWatched': ('django.db.models.fields.BigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_watchrecord'", 'to': "orm['website.User']"}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_watchrecord'", 'to': "orm['website.Video']"})
        }
    }

    complete_apps = ['website']