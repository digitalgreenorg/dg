# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Call'
        db.create_table(u'ivr_call', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exotel_call_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('attributes', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'ivr', ['Call'])


    def backwards(self, orm):
        # Deleting model 'Call'
        db.delete_table(u'ivr_call')


    models = {
        u'ivr.call': {
            'Meta': {'object_name': 'Call'},
            'attributes': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'exotel_call_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ivr']