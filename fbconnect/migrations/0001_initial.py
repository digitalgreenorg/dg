# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FBUser'
        db.create_table('fb_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fuid', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'fbconnect', ['FBUser'])

        # Adding model 'FBFollowers'
        db.create_table('fb_followers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fbuser', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('person', self.gf('dashboard.fields.fields.PositiveBigIntegerField')(null=True)),
        ))
        db.send_create_signal(u'fbconnect', ['FBFollowers'])


    def backwards(self, orm):
        # Deleting model 'FBUser'
        db.delete_table('fb_user')

        # Deleting model 'FBFollowers'
        db.delete_table('fb_followers')


    models = {
        u'fbconnect.fbfollowers': {
            'Meta': {'object_name': 'FBFollowers', 'db_table': "'fb_followers'"},
            'fbuser': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.fields.PositiveBigIntegerField', [], {'null': 'True'})
        },
        u'fbconnect.fbuser': {
            'Meta': {'object_name': 'FBUser', 'db_table': "'fb_user'"},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fuid': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fbconnect']