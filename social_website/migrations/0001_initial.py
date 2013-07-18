# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Partner'
        db.create_table('social_website_partner', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coco_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('joinDate', self.gf('django.db.models.fields.DateField')()),
            ('logoURL', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('websiteURL', self.gf('django.db.models.fields.URLField')(max_length=100, blank=True)),
            ('collection_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('video_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('views', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('likes', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('adoptions', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('social_website', ['Partner'])

        # Adding model 'Video'
        db.create_table('social_website_video', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coco_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('thumbnailURL16by9', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('onlineLikes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('offlineLikes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('onlineViews', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('offlineViews', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adoptions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subcategory', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subtopic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Partner'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('social_website', ['Video'])

        # Adding model 'Person'
        db.create_table('social_website_person', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coco_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=100)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Partner'])),
        ))
        db.send_create_signal('social_website', ['Person'])

        # Adding model 'PersonVideoRecord'
        db.create_table('social_website_personvideorecord', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('personID', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('videoID', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('views', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('like', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('adopted', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('social_website', ['PersonVideoRecord'])

        # Adding model 'Comment'
        db.create_table('social_website_comment', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('isOnline', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Video'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Person'])),
        ))
        db.send_create_signal('social_website', ['Comment'])

        # Adding model 'Collection'
        db.create_table('social_website_collection', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Partner'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subcategory', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subtopic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adoptions', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('social_website', ['Collection'])

        # Adding M2M table for field videos on 'Collection'
        db.create_table('social_website_collection_videos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm['social_website.collection'], null=False)),
            ('video', models.ForeignKey(orm['social_website.video'], null=False))
        ))
        db.create_unique('social_website_collection_videos', ['collection_id', 'video_id'])

        # Adding model 'FeaturedCollection'
        db.create_table('social_website_featuredcollection', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Collection'])),
            ('collageURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('social_website', ['FeaturedCollection'])

        # Adding model 'ImageSpec'
        db.create_table('social_website_imagespec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imageURL', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('altString', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('imageLinkURL', self.gf('django.db.models.fields.URLField')(max_length=400)),
        ))
        db.send_create_signal('social_website', ['ImageSpec'])

        # Adding model 'Activity'
        db.create_table('social_website_activity', (
            ('uid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('textContent', self.gf('django.db.models.fields.TextField')()),
            ('facebookID', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('avatarURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Partner'], null=True, blank=True)),
            ('farmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Person'], null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Collection'], null=True, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_website.Video'], null=True, blank=True)),
            ('newsfeeed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('social_website', ['Activity'])

        # Adding M2M table for field images on 'Activity'
        db.create_table('social_website_activity_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['social_website.activity'], null=False)),
            ('imagespec', models.ForeignKey(orm['social_website.imagespec'], null=False))
        ))
        db.create_unique('social_website_activity_images', ['activity_id', 'imagespec_id'])


    def backwards(self, orm):
        # Deleting model 'Partner'
        db.delete_table('social_website_partner')

        # Deleting model 'Video'
        db.delete_table('social_website_video')

        # Deleting model 'Person'
        db.delete_table('social_website_person')

        # Deleting model 'PersonVideoRecord'
        db.delete_table('social_website_personvideorecord')

        # Deleting model 'Comment'
        db.delete_table('social_website_comment')

        # Deleting model 'Collection'
        db.delete_table('social_website_collection')

        # Removing M2M table for field videos on 'Collection'
        db.delete_table('social_website_collection_videos')

        # Deleting model 'FeaturedCollection'
        db.delete_table('social_website_featuredcollection')

        # Deleting model 'ImageSpec'
        db.delete_table('social_website_imagespec')

        # Deleting model 'Activity'
        db.delete_table('social_website_activity')

        # Removing M2M table for field images on 'Activity'
        db.delete_table('social_website_activity_images')


    models = {
        'social_website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Collection']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Person']", 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social_website.ImageSpec']", 'null': 'True', 'blank': 'True'}),
            'newsfeeed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social_website.Partner']", 'null': 'True', 'blank': 'True'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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