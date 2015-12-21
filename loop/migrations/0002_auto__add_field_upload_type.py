# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Upload.type'
        db.add_column(u'loop_upload', 'type',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Upload.type'
        db.delete_column(u'loop_upload', 'type')


    models = {
        u'loop.upload': {
            'Meta': {'object_name': 'Upload'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediator': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'})
        }
    }

    complete_apps = ['loop']