# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'CombinedTransaction', fields ['date', 'farmer', 'crop', 'mandi', 'price', 'gaddidar', 'quantity', 'timestamp']
        db.delete_unique(u'loop_combinedtransaction', ['date', 'farmer_id', 'crop_id', 'mandi_id', 'price', 'gaddidar_id', 'quantity', 'timestamp'])

        # Adding unique constraint on 'CombinedTransaction', fields ['date', 'user_created', 'timestamp']
        db.create_unique(u'loop_combinedtransaction', ['date', 'user_created_id', 'timestamp'])


    def backwards(self, orm):
        # Removing unique constraint on 'CombinedTransaction', fields ['date', 'user_created', 'timestamp']
        db.delete_unique(u'loop_combinedtransaction', ['date', 'user_created_id', 'timestamp'])

        # Adding unique constraint on 'CombinedTransaction', fields ['date', 'farmer', 'crop', 'mandi', 'price', 'gaddidar', 'quantity', 'timestamp']
        db.create_unique(u'loop_combinedtransaction', ['date', 'farmer_id', 'crop_id', 'mandi_id', 'price', 'gaddidar_id', 'quantity', 'timestamp'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'loop.block': {
            'Meta': {'unique_together': "(('block_name', 'district'),)", 'object_name': 'Block'},
            'block_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_block_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_block_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.combinedtransaction': {
            'Meta': {'unique_together': "(('date', 'user_created', 'timestamp'),)", 'object_name': 'CombinedTransaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Crop']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Farmer']"}),
            'gaddidar': ('django.db.models.fields.related.ForeignKey', [], {'default': 'True', 'to': u"orm['loop.Gaddidar']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Mandi']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_combinedtransaction_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_combinedtransaction_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.country': {
            'Meta': {'unique_together': "(('country_name',),)", 'object_name': 'Country'},
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_country_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_country_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.crop': {
            'Meta': {'unique_together': "(('crop_name',),)", 'object_name': 'Crop'},
            'crop_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'measuring_unit': ('django.db.models.fields.CharField', [], {'default': "'kg'", 'max_length': '20'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_crop_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_crop_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.daytransportation': {
            'Meta': {'object_name': 'DayTransportation'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer_share': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Mandi']"}),
            'other_cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'transportation_cost': ('django.db.models.fields.FloatField', [], {}),
            'transportation_vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.TransportationVehicle']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_daytransportation_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_daytransportation_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'vrp_fees': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'loop.district': {
            'Meta': {'unique_together': "(('district_name', 'state'),)", 'object_name': 'District'},
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.State']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_district_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_district_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.farmer': {
            'Meta': {'unique_together': "(('phone', 'name'),)", 'object_name': 'Farmer'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_farmer_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_farmer_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Village']"})
        },
        u'loop.gaddidar': {
            'Meta': {'unique_together': "(('gaddidar_phone', 'gaddidar_name'),)", 'object_name': 'Gaddidar'},
            'commission': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'gaddidar_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gaddidar_phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mandi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Mandi']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_gaddidar_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_gaddidar_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.log': {
            'Meta': {'object_name': 'Log'},
            'action': ('django.db.models.fields.IntegerField', [], {}),
            'entry_table': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loop_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.LoopUser']", 'null': 'True'}),
            'model_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'village': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'loop.loopuser': {
            'Meta': {'object_name': 'LoopUser'},
            'assigned_mandis': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_mandis'", 'to': u"orm['loop.Mandi']", 'through': u"orm['loop.LoopUserAssignedMandi']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_villages'", 'to': u"orm['loop.Village']", 'through': u"orm['loop.LoopUserAssignedVillage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mode': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '100'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '14'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'loop_user'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuser_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuser_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['loop.Village']", 'null': 'True'})
        },
        u'loop.loopuserassignedmandi': {
            'Meta': {'object_name': 'LoopUserAssignedMandi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'loop_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.LoopUser']"}),
            'mandi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Mandi']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuserassignedmandi_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuserassignedmandi_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.loopuserassignedvillage': {
            'Meta': {'object_name': 'LoopUserAssignedVillage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'loop_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.LoopUser']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuserassignedvillage_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuserassignedvillage_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Village']"})
        },
        u'loop.mandi': {
            'Meta': {'unique_together': "(('mandi_name', 'district'),)", 'object_name': 'Mandi'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'mandi_name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_mandi_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_mandi_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.state': {
            'Meta': {'unique_together': "(('state_name',),)", 'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_state_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_state_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.transportationvehicle': {
            'Meta': {'unique_together': "(('transporter', 'vehicle', 'vehicle_number'),)", 'object_name': 'TransportationVehicle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'transporter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Transporter']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_transportationvehicle_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_transportationvehicle_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Vehicle']"}),
            'vehicle_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'loop.transporter': {
            'Meta': {'unique_together': "(('transporter_name', 'transporter_phone'),)", 'object_name': 'Transporter'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Block']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'transporter_name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'transporter_phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_transporter_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_transporter_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.vehicle': {
            'Meta': {'unique_together': "(('vehicle_name',),)", 'object_name': 'Vehicle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_vehicle_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_vehicle_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'vehicle_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'loop.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Block']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_village_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_village_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['loop']