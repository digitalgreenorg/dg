# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Milestone'
        db.create_table('social_website_milestone', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Partner'], unique=True)),
            ('videoNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('villageNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('screeningNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('viewerNumber', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('social_website', ['Milestone'])

        # Adding field 'Activity.type'
        db.add_column('social_website_activity', 'type',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Activity.titleURL'
        db.add_column('social_website_activity', 'titleURL',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=400),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Milestone'
        db.delete_table('social_website_milestone')

        # Deleting field 'Activity.type'
        db.delete_column('social_website_activity', 'type')

        # Deleting field 'Activity.titleURL'
        db.delete_column('social_website_activity', 'titleURL')


    models = {
        'social_website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Collection']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Person']", 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social_website.ImageSpec']", 'null': 'True', 'blank': 'True'}),
            'newsFeed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']", 'null': 'True', 'blank': 'True'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'titleURL': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Video']", 'null': 'True', 'blank': 'True'})
        },
        'social_website.collection': {
            'Meta': {'object_name': 'Collection'},
            'adoptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['social_website.Video']", 'symmetrical': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'social_website.comment': {
            'Meta': {'object_name': 'Comment'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Person']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Video']"})
        },
        'social_website.featuredcollection': {
            'Meta': {'object_name': 'FeaturedCollection'},
            'collageURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Collection']"}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social_website.imagespec': {
            'Meta': {'object_name': 'ImageSpec'},
            'altString': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageLinkURL': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '400'})
        },
        'social_website.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']", 'unique': 'True'}),
            'screeningNumber': ('django.db.models.fields.IntegerField', [], {}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videoNumber': ('django.db.models.fields.IntegerField', [], {}),
            'viewerNumber': ('django.db.models.fields.IntegerField', [], {}),
            'villageNumber': ('django.db.models.fields.IntegerField', [], {})
        },
        'social_website.partner': {
            'Meta': {'object_name': 'Partner'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'coco_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'collection_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'joinDate': ('django.db.models.fields.DateField', [], {}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'logoURL': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'websiteURL': ('django.db.models.fields.URLField', [], {'max_length': '100', 'blank': 'True'})
        },
        'social_website.person': {
            'Meta': {'object_name': 'Person'},
            'coco_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']"}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'social_website.personvideorecord': {
            'Meta': {'object_name': 'PersonVideoRecord'},
            'adopted': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'personID': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'videoID': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'views': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'social_website.video': {
            'Meta': {'object_name': 'Video'},
            'adoptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'coco_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'offlineLikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'offlineViews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'onlineLikes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'onlineViews': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'thumbnailURL16by9': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['social_website']