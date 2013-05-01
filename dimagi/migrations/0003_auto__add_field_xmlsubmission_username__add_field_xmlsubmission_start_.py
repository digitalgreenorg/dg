# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'XMLSubmission.username'
        db.add_column('dimagi_xmlsubmission', 'username',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'XMLSubmission.start_time'
        db.add_column('dimagi_xmlsubmission', 'start_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'XMLSubmission.end_time'
        db.add_column('dimagi_xmlsubmission', 'end_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'XMLSubmission.username'
        db.delete_column('dimagi_xmlsubmission', 'username')

        # Deleting field 'XMLSubmission.start_time'
        db.delete_column('dimagi_xmlsubmission', 'start_time')

        # Deleting field 'XMLSubmission.end_time'
        db.delete_column('dimagi_xmlsubmission', 'end_time')


    models = {
        'dimagi.xmlsubmission': {
            'Meta': {'object_name': 'XMLSubmission'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'submission_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'xml_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dimagi']