# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Upload'
        db.create_table(u'loop_upload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('mediator', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'loop', ['Upload'])


    def backwards(self, orm):
        # Deleting model 'Upload'
        db.delete_table(u'loop_upload')


    models = {
        u'loop.upload': {
            'Meta': {'object_name': 'Upload'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediator': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['loop']