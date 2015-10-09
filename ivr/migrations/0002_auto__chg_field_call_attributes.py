# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Call.attributes'
        db.alter_column(u'ivr_call', 'attributes', self.gf('django.db.models.fields.CharField')(max_length=500))

    def backwards(self, orm):

        # Changing field 'Call.attributes'
        db.alter_column(u'ivr_call', 'attributes', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'ivr.call': {
            'Meta': {'object_name': 'Call'},
            'attributes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'exotel_call_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ivr']