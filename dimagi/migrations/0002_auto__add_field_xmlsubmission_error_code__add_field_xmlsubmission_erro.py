# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'XMLSubmission.error_code'
        db.add_column('dimagi_xmlsubmission', 'error_code',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'XMLSubmission.error_message'
        db.add_column('dimagi_xmlsubmission', 'error_message',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'XMLSubmission.error_code'
        db.delete_column('dimagi_xmlsubmission', 'error_code')

        # Deleting field 'XMLSubmission.error_message'
        db.delete_column('dimagi_xmlsubmission', 'error_message')


    models = {
        'dimagi.xmlsubmission': {
            'Meta': {'object_name': 'XMLSubmission'},
            'error_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submission_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'xml_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dimagi']