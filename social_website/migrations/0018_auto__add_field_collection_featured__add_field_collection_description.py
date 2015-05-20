# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Collection.featured'
        db.add_column(u'social_website_collection', 'featured',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Collection.description'
        db.add_column(u'social_website_collection', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Collection.featured'
        db.delete_column(u'social_website_collection', 'featured')

        # Deleting field 'Collection.description'
        db.delete_column(u'social_website_collection', 'description')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'social_website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Collection']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Person']", 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['social_website.ImageSpec']", 'null': 'True', 'blank': 'True'}),
            'newsFeed': ('django.db.models.fields.BooleanField', [], {}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Partner']", 'null': 'True', 'blank': 'True'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'titleURL': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Video']", 'null': 'True', 'blank': 'True'})
        },
        u'social_website.collection': {
            'Meta': {'unique_together': "(('title', 'partner', 'state', 'language'),)", 'object_name': 'Collection'},
            'adoptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['social_website.Video']", 'through': u"orm['social_website.VideoinCollection']", 'symmetrical': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'social_website.comment': {
            'Meta': {'object_name': 'Comment'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 3, 11, 0, 0)'}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Person']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Video']"})
        },
        u'social_website.crontimestamp': {
            'Meta': {'object_name': 'CronTimestamp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 11, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'social_website.featuredcollection': {
            'Meta': {'object_name': 'FeaturedCollection'},
            'collageURL': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Collection']"}),
            'show_on_homepage': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_on_language_selection': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'social_website.imagespec': {
            'Meta': {'object_name': 'ImageSpec'},
            'altString': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageLinkURL': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '400'})
        },
        u'social_website.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Partner']", 'unique': 'True'}),
            'screeningNumber': ('django.db.models.fields.IntegerField', [], {}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videoNumber': ('django.db.models.fields.IntegerField', [], {}),
            'viewerNumber': ('django.db.models.fields.IntegerField', [], {}),
            'villageNumber': ('django.db.models.fields.IntegerField', [], {})
        },
        u'social_website.partner': {
            'Meta': {'object_name': 'Partner'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'coco_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'collection_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'joinDate': ('django.db.models.fields.DateField', [], {}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'location_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logoURL': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'websiteURL': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '100'})
        },
        u'social_website.person': {
            'Meta': {'object_name': 'Person'},
            'coco_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Partner']"}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'social_website.personvideorecord': {
            'Meta': {'object_name': 'PersonVideoRecord'},
            'adopted': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'personID': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videoID': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'views': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'social_website.video': {
            'Meta': {'object_name': 'Video'},
            'adoptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'coco_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'offlineLikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'offlineViews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'onlineLikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'onlineViews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailURL16by9': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'social_website.videoincollection': {
            'Meta': {'ordering': "['order']", 'object_name': 'VideoinCollection'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Collection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Video']"})
        },
        u'social_website.videolike': {
            'Meta': {'object_name': 'VideoLike'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_website.Video']"})
        }
    }

    complete_apps = ['social_website']