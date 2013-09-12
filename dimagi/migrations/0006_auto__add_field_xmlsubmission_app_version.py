# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'XMLSubmission.app_version'
        db.add_column('dimagi_xmlsubmission', 'app_version',
                      self.gf('django.db.models.fields.IntegerField')(default='0'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'XMLSubmission.app_version'
        db.delete_column('dimagi_xmlsubmission', 'app_version')


    models = {
        'dimagi.xmlsubmission': {
            'Meta': {'object_name': 'XMLSubmission'},
            'app_version': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'submission_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'username': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'xml_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dimagi']