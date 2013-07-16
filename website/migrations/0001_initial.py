# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('website_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('countryName', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Country'])

        # Adding model 'Interests'
        db.create_table('website_interests', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('website', ['Interests'])

        # Adding model 'Tag'
        db.create_table('website_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Tag'])

        # Adding model 'Badge'
        db.create_table('website_badge', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Badge'])

        # Adding model 'User'
        db.create_table('website_user', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('avatarURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebookID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('twitterID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('linkedInID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('authToken', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('website', ['User'])

        # Adding model 'Partner'
        db.create_table('website_partner', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('joinDate', self.gf('django.db.models.fields.DateField')()),
            ('logoURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('collectionCount', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('videos', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('views', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('likes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('adoptions', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('website', ['Partner'])

        # Adding model 'Language'
        db.create_table('website_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Language'])

        # Adding model 'Video'
        db.create_table('website_video', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('duration', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('onlineLikes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('offlineLikes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('onlineViews', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('offlineViews', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('adoptions', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subsector', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subtopic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_videos', to=orm['website.Partner'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='language_videos', max_length=20, to=orm['website.Language'])),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('website', ['Video'])

        # Adding M2M table for field tags on 'Video'
        db.create_table('website_video_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('video', models.ForeignKey(orm['website.video'], null=False)),
            ('tag', models.ForeignKey(orm['website.tag'], null=False))
        ))
        db.create_unique('website_video_tags', ['video_id', 'tag_id'])

        # Adding model 'Collection'
        db.create_table('website_collection', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_collections', to=orm['website.Country'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_collections', to=orm['website.Partner'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='language_collections', max_length=20, to=orm['website.Language'])),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subcategory', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subtopic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('website', ['Collection'])

        # Adding M2M table for field videos on 'Collection'
        db.create_table('website_collection_videos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm['website.collection'], null=False)),
            ('video', models.ForeignKey(orm['website.video'], null=False))
        ))
        db.create_unique('website_collection_videos', ['collection_id', 'video_id'])

        # Adding model 'Farmer'
        db.create_table('website_farmer', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=100)),
            ('village', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Partner'])),
        ))
        db.send_create_signal('website', ['Farmer'])

        # Adding M2M table for field interests on 'Farmer'
        db.create_table('website_farmer_interests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farmer', models.ForeignKey(orm['website.farmer'], null=False)),
            ('interests', models.ForeignKey(orm['website.interests'], null=False))
        ))
        db.create_unique('website_farmer_interests', ['farmer_id', 'interests_id'])

        # Adding M2M table for field collections on 'Farmer'
        db.create_table('website_farmer_collections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farmer', models.ForeignKey(orm['website.farmer'], null=False)),
            ('collection', models.ForeignKey(orm['website.collection'], null=False))
        ))
        db.create_unique('website_farmer_collections', ['farmer_id', 'collection_id'])

        # Adding model 'ImageSpec'
        db.create_table('website_imagespec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imageURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('altString', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('imageLinkURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('website', ['ImageSpec'])

        # Adding model 'Activity'
        db.create_table('website_activity', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('textContent', self.gf('django.db.models.fields.TextField')()),
            ('avatarURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Partner'], null=True, blank=True)),
            ('farmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Farmer'], null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Collection'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.User'], null=True, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Video'])),
        ))
        db.send_create_signal('website', ['Activity'])

        # Adding M2M table for field images on 'Activity'
        db.create_table('website_activity_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['website.activity'], null=False)),
            ('imagespec', models.ForeignKey(orm['website.imagespec'], null=False))
        ))
        db.create_unique('website_activity_images', ['activity_id', 'imagespec_id'])

        # Adding model 'Comment'
        db.create_table('website_comment', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('isOnline', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_comments', null=True, to=orm['website.User'])),
            ('inReplyToCommentUID', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='replies', null=True, to=orm['website.Comment'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='video_comments', null=True, to=orm['website.Video'])),
            ('farmer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='farmer_comments', null=True, to=orm['website.Farmer'])),
            ('activityURI', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comment_activity', null=True, to=orm['website.Activity'])),
        ))
        db.send_create_signal('website', ['Comment'])

        # Adding model 'FilterValueDescription'
        db.create_table('website_filtervaluedescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('itemCount', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('website', ['FilterValueDescription'])

        # Adding model 'SearchCompletion'
        db.create_table('website_searchcompletion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('searchTerm', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('targetURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('website', ['SearchCompletion'])

        # Adding model 'VideoWatchRecord'
        db.create_table('website_videowatchrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('videoUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video_watchrecord', to=orm['website.Video'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_watchrecord', to=orm['website.User'])),
            ('timeWatched', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('website', ['VideoWatchRecord'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table('website_country')

        # Deleting model 'Interests'
        db.delete_table('website_interests')

        # Deleting model 'Tag'
        db.delete_table('website_tag')

        # Deleting model 'Badge'
        db.delete_table('website_badge')

        # Deleting model 'User'
        db.delete_table('website_user')

        # Deleting model 'Partner'
        db.delete_table('website_partner')

        # Deleting model 'Language'
        db.delete_table('website_language')

        # Deleting model 'Video'
        db.delete_table('website_video')

        # Removing M2M table for field tags on 'Video'
        db.delete_table('website_video_tags')

        # Deleting model 'Collection'
        db.delete_table('website_collection')

        # Removing M2M table for field videos on 'Collection'
        db.delete_table('website_collection_videos')

        # Deleting model 'Farmer'
        db.delete_table('website_farmer')

        # Removing M2M table for field interests on 'Farmer'
        db.delete_table('website_farmer_interests')

        # Removing M2M table for field collections on 'Farmer'
        db.delete_table('website_farmer_collections')

        # Deleting model 'ImageSpec'
        db.delete_table('website_imagespec')

        # Deleting model 'Activity'
        db.delete_table('website_activity')

        # Removing M2M table for field images on 'Activity'
        db.delete_table('website_activity_images')

        # Deleting model 'Comment'
        db.delete_table('website_comment')

        # Deleting model 'FilterValueDescription'
        db.delete_table('website_filtervaluedescription')

        # Deleting model 'SearchCompletion'
        db.delete_table('website_searchcompletion')

        # Deleting model 'VideoWatchRecord'
        db.delete_table('website_videowatchrecord')


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
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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