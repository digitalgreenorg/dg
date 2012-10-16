# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PathLog'
        db.create_table('path_pathlog', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('person_offline_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('person_online_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('path', ['PathLog'])


    def backwards(self, orm):
        # Deleting model 'PathLog'
        db.delete_table('path_pathlog')


    models = {
        'path.pathlog': {
            'Meta': {'object_name': 'PathLog'},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person_offline_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'person_online_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['path']