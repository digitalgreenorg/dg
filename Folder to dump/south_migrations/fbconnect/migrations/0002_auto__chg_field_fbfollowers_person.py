# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FBFollowers.person'
        db.alter_column('fb_followers', 'person', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

    def backwards(self, orm):

        # Changing field 'FBFollowers.person'
        db.alter_column('fb_followers', 'person', self.gf('dashboard.fields.fields.PositiveBigIntegerField')(null=True))

    models = {
        u'fbconnect.fbfollowers': {
            'Meta': {'object_name': 'FBFollowers', 'db_table': "'fb_followers'"},
            'fbuser': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True'})
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