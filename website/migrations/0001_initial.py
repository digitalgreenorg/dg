# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Video'
        db.create_table('website_video', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('youtubeID', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('duration', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('onlineLikes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('offlineLikes', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('onlineViews', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('offlineViews', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('adoptions', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Video'])

        # Adding model 'Country'
        db.create_table('website_country', (
            ('countryCode', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('countryName', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('website', ['Country'])

        # Adding model 'Farmer'
        db.create_table('website_farmer', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('imageURL', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('village', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_farmers', to=orm['website.Country'])),
        ))
        db.send_create_signal('website', ['Farmer'])

        # Adding model 'Partner'
        db.create_table('website_partner', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('joinDate', self.gf('django.db.models.fields.DateField')()),
            ('logoURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
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

        # Adding model 'Collection'
        db.create_table('website_collection', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('thumbnailURL', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_collections', to=orm['website.Country'])),
            ('partnerUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_collections', to=orm['website.Partner'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sector', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('subsector', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
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
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('textContent', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('avatarURL', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('collectionUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collection_activity', blank=True, to=orm['website.Collection'])),
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

        # Adding model 'Language'
        db.create_table('website_language', (
            ('countryCode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Country'])),
            ('languageCode', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('website', ['Language'])

        # Adding model 'Person'
        db.create_table('website_person', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('website', ['Person'])

        # Adding model 'Comment'
        db.create_table('website_comment', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('isOnline', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('partnerUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partner_comments', to=orm['website.Partner'])),
            ('personUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_comments', to=orm['website.Person'])),
            ('inReplyToCommentUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', to=orm['website.Comment'])),
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

        # Adding model 'UserInfo'
        db.create_table('website_userinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('personUID', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_userinfo', to=orm['website.Person'])),
            ('avatarURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('website', ['UserInfo'])


    def backwards(self, orm):
        # Deleting model 'Video'
        db.delete_table('website_video')

        # Deleting model 'Country'
        db.delete_table('website_country')

        # Deleting model 'Farmer'
        db.delete_table('website_farmer')

        # Deleting model 'Partner'
        db.delete_table('website_partner')

        # Removing M2M table for field farmers on 'Partner'
        db.delete_table('website_partner_farmers')

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

        # Deleting model 'Language'
        db.delete_table('website_language')

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

        # Deleting model 'UserInfo'
        db.delete_table('website_userinfo')


    models = {
        'website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'collectionUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_activity'", 'blank': 'True', 'to': "orm['website.Collection']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['website.ImageSpec']", 'symmetrical': 'False'}),
            'textContent': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeVideoID': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'website.collection': {
            'Meta': {'object_name': 'Collection'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_collections'", 'to': "orm['website.Country']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'partnerUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_collections'", 'to': "orm['website.Partner']"}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subsector': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnailURL': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_collections'", 'symmetrical': 'False', 'to': "orm['website.Video']"})
        },
        'website.comment': {
            'Meta': {'object_name': 'Comment'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'inReplyToCommentUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': "orm['website.Comment']"}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'partnerUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_comments'", 'to': "orm['website.Partner']"}),
            'personUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_comments'", 'to': "orm['website.Person']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.country': {
            'Meta': {'object_name': 'Country'},
            'countryCode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'countryName': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.farmer': {
            'Meta': {'object_name': 'Farmer'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_farmers'", 'to': "orm['website.Country']"}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'imageURL': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'thumbnailURL': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        'website.language': {
            'Meta': {'object_name': 'Language'},
            'countryCode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Country']"}),
            'languageCode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.partner': {
            'Meta': {'object_name': 'Partner'},
            'collectionCount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'farmers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'farmer_partner'", 'symmetrical': 'False', 'to': "orm['website.Farmer']"}),
            'joinDate': ('django.db.models.fields.DateField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'logoURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.person': {
            'Meta': {'object_name': 'Person'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.searchcompletion': {
            'Meta': {'object_name': 'SearchCompletion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'searchTerm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'website.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'personUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_userinfo'", 'to': "orm['website.Person']"})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'duration': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offlineLikes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offlineViews': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineLikes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineViews': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnailURL': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
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