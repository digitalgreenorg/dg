# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'XMLSubmission'
        db.create_table('dimagi_xmlsubmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submission_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modification_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('xml_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dimagi', ['XMLSubmission'])


    def backwards(self, orm):
        # Deleting model 'XMLSubmission'
        db.delete_table('dimagi_xmlsubmission')


    models = {
        'dimagi.xmlsubmission': {
            'Meta': {'object_name': 'XMLSubmission'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submission_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'xml_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dimagi']