# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('website_country', (
            ('countryCode', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('countryName', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Country'])

        # Adding model 'Interest'
        db.create_table('website_interest', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('website', ['Interest'])

        # Adding model 'Farmer'
        db.create_table('website_farmer', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('imageURL', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('village', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Farmer'])

        # Adding M2M table for field interests on 'Farmer'
        db.create_table('website_farmer_interests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('farmer', models.ForeignKey(orm['website.farmer'], null=False)),
            ('interest', models.ForeignKey(orm['website.interest'], null=False))
        ))
        db.create_unique('website_farmer_interests', ['farmer_id', 'interest_id'])

        # Adding model 'Partner'
        db.create_table('website_partner', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('joinDate', self.gf('django.db.models.fields.DateField')()),
            ('logoURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('collectionCount', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('website', ['Partner'])

        # Adding M2M table for field farmers on 'Partner'
        db.create_table('website_partner_farmers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['website.partner'], null=False)),
            ('farmer', models.ForeignKey(orm['website.farmer'], null=False))
        ))
        db.create_unique('website_partner_farmers', ['partner_id', 'farmer_id'])

        # Adding model 'Language'
        db.create_table('website_language', (
            ('languageCode', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Language'])

        # Adding model 'Video'
        db.create_table('website_video', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('duration', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('onlineLikes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('offlineLikes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('onlineViews', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('offlineViews', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('adoptions', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subsector', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('partnerUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_videos', to=orm['website.Partner'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='language_videos', max_length=20, to=orm['website.Language'])),
        ))
        db.send_create_signal('website', ['Video'])

        # Adding model 'Collection'
        db.create_table('website_collection', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('thumbnailURL', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_collections', to=orm['website.Country'])),
            ('partnerUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_collections', to=orm['website.Partner'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(related_name='language_collections', max_length=20, to=orm['website.Language'])),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('subsector', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
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

        # Adding model 'ImageSpec'
        db.create_table('website_imagespec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imageURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('website', ['ImageSpec'])

        # Adding model 'Activity'
        db.create_table('website_activity', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('textContent', self.gf('django.db.models.fields.TextField')()),
            ('avatarURL', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('youtubeVideoID', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('website', ['Activity'])

        # Adding M2M table for field images on 'Activity'
        db.create_table('website_activity_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['website.activity'], null=False)),
            ('imagespec', models.ForeignKey(orm['website.imagespec'], null=False))
        ))
        db.create_unique('website_activity_images', ['activity_id', 'imagespec_id'])

        # Adding model 'Person'
        db.create_table('website_person', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('avatarURL', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebookID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('twitterID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('linkedInID', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('authToken', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('website', ['Person'])

        # Adding model 'Comment'
        db.create_table('website_comment', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('isOnline', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('partnerUID', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='partner_comments', null=True, to=orm['website.Partner'])),
            ('personUID', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='person_comments', null=True, to=orm['website.Person'])),
            ('inReplyToCommentUID', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='replies', null=True, to=orm['website.Comment'])),
            ('videoUID', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='video_comments', null=True, to=orm['website.Video'])),
            ('farmerUID', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='farmer_comments', null=True, to=orm['website.Video'])),
        ))
        db.send_create_signal('website', ['Comment'])

        # Adding model 'FilterValueDescription'
        db.create_table('website_filtervaluedescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('itemCount', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('website', ['FilterValueDescription'])

        # Adding model 'SearchCompletion'
        db.create_table('website_searchcompletion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('searchTerm', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['SearchCompletion'])

        # Adding model 'VideoWatchRecord'
        db.create_table('website_videowatchrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('videoUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='video_watchrecord', to=orm['website.Video'])),
            ('personUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_watchrecord', to=orm['website.Person'])),
            ('timeWatched', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('website', ['VideoWatchRecord'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table('website_country')

        # Deleting model 'Interest'
        db.delete_table('website_interest')

        # Deleting model 'Farmer'
        db.delete_table('website_farmer')

        # Removing M2M table for field interests on 'Farmer'
        db.delete_table('website_farmer_interests')

        # Deleting model 'Partner'
        db.delete_table('website_partner')

        # Removing M2M table for field farmers on 'Partner'
        db.delete_table('website_partner_farmers')

        # Deleting model 'Language'
        db.delete_table('website_language')

        # Deleting model 'Video'
        db.delete_table('website_video')

        # Deleting model 'Collection'
        db.delete_table('website_collection')

        # Removing M2M table for field videos on 'Collection'
        db.delete_table('website_collection_videos')

        # Deleting model 'ImageSpec'
        db.delete_table('website_imagespec')

        # Deleting model 'Activity'
        db.delete_table('website_activity')

        # Removing M2M table for field images on 'Activity'
        db.delete_table('website_activity_images')

        # Deleting model 'Person'
        db.delete_table('website_person')

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
            'farmerUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmer_comments'", 'null': 'True', 'to': "orm['website.Video']"}),
            'inReplyToCommentUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['website.Comment']"}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'partnerUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partner_comments'", 'null': 'True', 'to': "orm['website.Partner']"}),
            'personUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'person_comments'", 'null': 'True', 'to': "orm['website.Person']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_comments'", 'null': 'True', 'to': "orm['website.Video']"})
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
        'website.videowatchrecord': {
            'Meta': {'object_name': 'VideoWatchRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'personUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_watchrecord'", 'to': "orm['website.Person']"}),
            'timeWatched': ('django.db.models.fields.BigIntegerField', [], {}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_watchrecord'", 'to': "orm['website.Video']"})
        }
    }

    complete_apps = ['website']