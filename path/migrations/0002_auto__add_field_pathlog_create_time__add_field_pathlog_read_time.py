# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PathLog.create_time'
        db.add_column('path_pathlog', 'create_time',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 10, 17, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'PathLog.read_time'
        db.add_column('path_pathlog', 'read_time',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 10, 17, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PathLog.create_time'
        db.delete_column('path_pathlog', 'create_time')

        # Deleting field 'PathLog.read_time'
        db.delete_column('path_pathlog', 'read_time')


    models = {
        'path.pathlog': {
            'Meta': {'object_name': 'PathLog'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person_offline_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'person_online_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'read_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['path']