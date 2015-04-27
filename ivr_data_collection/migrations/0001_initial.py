# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomFieldTest'
        db.create_table(u'ivr_data_collection_customfieldtest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('CustomField', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal(u'ivr_data_collection', ['CustomFieldTest'])


    def backwards(self, orm):
        # Deleting model 'CustomFieldTest'
        db.delete_table(u'ivr_data_collection_customfieldtest')


    models = {
        u'ivr_data_collection.customfieldtest': {
            'CustomField': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'Meta': {'object_name': 'CustomFieldTest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        }
    }

    complete_apps = ['ivr_data_collection']