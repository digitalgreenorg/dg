# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CommentLike'
        db.create_table('website_commentlike', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('commentUID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Comment'])),
            ('userUID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('website', ['CommentLike'])

        # Adding model 'TimeWatched'
        db.create_table('website_timewatched', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('videoWatchRecord', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.VideoWatchRecord'])),
        ))
        db.send_create_signal('website', ['TimeWatched'])

        # Adding model 'UserCollectionHistory'
        db.create_table('website_usercollectionhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userUID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('website', ['UserCollectionHistory'])

        # Adding M2M table for field completed on 'UserCollectionHistory'
        db.create_table('website_usercollectionhistory_completed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usercollectionhistory', models.ForeignKey(orm['website.usercollectionhistory'], null=False)),
            ('collection', models.ForeignKey(orm['website.collection'], null=False))
        ))
        db.create_unique('website_usercollectionhistory_completed', ['usercollectionhistory_id', 'collection_id'])

        # Adding M2M table for field recentlyViewed on 'UserCollectionHistory'
        db.create_table('website_usercollectionhistory_recentlyViewed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usercollectionhistory', models.ForeignKey(orm['website.usercollectionhistory'], null=False)),
            ('collection', models.ForeignKey(orm['website.collection'], null=False))
        ))
        db.create_unique('website_usercollectionhistory_recentlyViewed', ['usercollectionhistory_id', 'collection_id'])

        # Adding M2M table for field likedCollections on 'UserCollectionHistory'
        db.create_table('website_usercollectionhistory_likedCollections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usercollectionhistory', models.ForeignKey(orm['website.usercollectionhistory'], null=False)),
            ('collection', models.ForeignKey(orm['website.collection'], null=False))
        ))
        db.create_unique('website_usercollectionhistory_likedCollections', ['usercollectionhistory_id', 'collection_id'])

        # Adding model 'WebsiteUser'
        db.create_table('website_websiteuser', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('avatarURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebookID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('twitterID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('linkedInID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('authToken', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('website', ['WebsiteUser'])

        # Adding model 'VideoLike'
        db.create_table('website_videolike', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('videoUID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Video'])),
            ('userUID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('website', ['VideoLike'])


    def backwards(self, orm):
        # Deleting model 'CommentLike'
        db.delete_table('website_commentlike')

        # Deleting model 'TimeWatched'
        db.delete_table('website_timewatched')

        # Deleting model 'UserCollectionHistory'
        db.delete_table('website_usercollectionhistory')

        # Removing M2M table for field completed on 'UserCollectionHistory'
        db.delete_table('website_usercollectionhistory_completed')

        # Removing M2M table for field recentlyViewed on 'UserCollectionHistory'
        db.delete_table('website_usercollectionhistory_recentlyViewed')

        # Removing M2M table for field likedCollections on 'UserCollectionHistory'
        db.delete_table('website_usercollectionhistory_likedCollections')

        # Deleting model 'WebsiteUser'
        db.delete_table('website_websiteuser')

        # Deleting model 'VideoLike'
        db.delete_table('website_videolike')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['website.ImageSpec']", 'symmetrical': 'False'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeVideoID': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'website.collection': {
            'Meta': {'object_name': 'Collection'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_collections'", 'to': "orm['website.Country']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'language_collections'", 'max_length': '20', 'to': "orm['website.Language']"}),
            'partnerUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_collections'", 'to': "orm['website.Partner']"}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subsector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_collections'", 'symmetrical': 'False', 'to': "orm['website.Video']"})
        },
        'website.comment': {
            'Meta': {'object_name': 'Comment'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmerUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmer_comments'", 'null': 'True', 'to': "orm['website.Farmer']"}),
            'inReplyToCommentUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['website.Comment']"}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'partnerUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partner_comments'", 'null': 'True', 'to': "orm['website.Partner']"}),
            'personUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'person_comments'", 'null': 'True', 'to': "orm['website.Person']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_comments'", 'null': 'True', 'to': "orm['website.Video']"})
        },
        'website.commentlike': {
            'Meta': {'object_name': 'CommentLike'},
            'commentUID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Comment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userUID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'website.country': {
            'Meta': {'object_name': 'Country'},
            'countryCode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'countryName': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.farmer': {
            'Meta': {'object_name': 'Farmer'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'imageURL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'farmer_interests'", 'symmetrical': 'False', 'to': "orm['website.Interest']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnailURL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.filtervaluedescription': {
            'Meta': {'object_name': 'FilterValueDescription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemCount': ('django.db.models.fields.BigIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.imagespec': {
            'Meta': {'object_name': 'ImageSpec'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'website.interest': {
            'Meta': {'object_name': 'Interest'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.language': {
            'Meta': {'object_name': 'Language'},
            'languageCode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.partner': {
            'Meta': {'object_name': 'Partner'},
            'collectionCount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'farmers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'farmer_partner'", 'symmetrical': 'False', 'to': "orm['website.Farmer']"}),
            'joinDate': ('django.db.models.fields.DateField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'logoURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.person': {
            'Meta': {'object_name': 'Person'},
            'authToken': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'linkedInID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitterID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'website.searchcompletion': {
            'Meta': {'object_name': 'SearchCompletion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'searchTerm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'website.timewatched': {
            'Meta': {'object_name': 'TimeWatched'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videoWatchRecord': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.VideoWatchRecord']"})
        },
        'website.usercollectionhistory': {
            'Meta': {'object_name': 'UserCollectionHistory'},
            'completed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'completed'", 'symmetrical': 'False', 'to': "orm['website.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likedCollections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'liked'", 'symmetrical': 'False', 'to': "orm['website.Collection']"}),
            'recentlyViewed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'viewed'", 'symmetrical': 'False', 'to': "orm['website.Collection']"}),
            'userUID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'partnerUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_videos'", 'to': "orm['website.Partner']"}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subsector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.videolike': {
            'Meta': {'object_name': 'VideoLike'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userUID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        },
        'website.videowatchrecord': {
            'Meta': {'object_name': 'VideoWatchRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'personUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_watchrecord'", 'to': "orm['website.Person']"}),
            'timeWatched': ('django.db.models.fields.BigIntegerField', [], {}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_watchrecord'", 'to': "orm['website.Video']"})
        },
        'website.websiteuser': {
            'Meta': {'object_name': 'WebsiteUser'},
            'authToken': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'linkedInID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitterID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['website']