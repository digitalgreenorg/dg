# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CustomFieldTest.call_sid'
        db.add_column(u'ivr_data_collection_customfieldtest', 'call_sid',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CustomFieldTest.call_sid'
        db.delete_column(u'ivr_data_collection_customfieldtest', 'call_sid')


    models = {
        u'ivr_data_collection.customfieldtest': {
            'CustomField': ('django.db.models.fields.CharField', [], {'default': "'abc'", 'max_length': '20', 'null': 'True'}),
            'Meta': {'object_name': 'CustomFieldTest'},
            'call_sid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        }
    }

    complete_apps = ['ivr_data_collection']