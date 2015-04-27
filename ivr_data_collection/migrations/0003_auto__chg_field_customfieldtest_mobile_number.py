# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CustomFieldTest.mobile_number'
        db.alter_column(u'ivr_data_collection_customfieldtest', 'mobile_number', self.gf('django.db.models.fields.CharField')(max_length=11, null=True))

    def backwards(self, orm):

        # Changing field 'CustomFieldTest.mobile_number'
        db.alter_column(u'ivr_data_collection_customfieldtest', 'mobile_number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

    models = {
        u'ivr_data_collection.customfieldtest': {
            'CustomField': ('django.db.models.fields.CharField', [], {'default': "'abc'", 'max_length': '20', 'null': 'True'}),
            'Meta': {'object_name': 'CustomFieldTest'},
            'call_sid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True'})
        }
    }

    complete_apps = ['ivr_data_collection']