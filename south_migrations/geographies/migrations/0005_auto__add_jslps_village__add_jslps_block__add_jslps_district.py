# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JSLPS_Village'
        db.create_table(u'geographies_jslps_village', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_jslps_village_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_jslps_village_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('village_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('village_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Village', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.Village'], null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['JSLPS_Village'])

        # Adding model 'JSLPS_Block'
        db.create_table(u'geographies_jslps_block', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_jslps_block_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_jslps_block_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('district_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.Block'], null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['JSLPS_Block'])

        # Adding model 'JSLPS_District'
        db.create_table(u'geographies_jslps_district', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_jslps_district_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_jslps_district_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.District'], null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['JSLPS_District'])


    def backwards(self, orm):
        # Deleting model 'JSLPS_Village'
        db.delete_table(u'geographies_jslps_village')

        # Deleting model 'JSLPS_Block'
        db.delete_table(u'geographies_jslps_block')

        # Deleting model 'JSLPS_District'
        db.delete_table(u'geographies_jslps_district')


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
        u'geographies.block': {
            'Meta': {'object_name': 'Block'},
            'block_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_block_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_block_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.country': {
            'Meta': {'object_name': 'Country'},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_country_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_country_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.district': {
            'Meta': {'object_name': 'District'},
            'district_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '31', 'decimal_places': '28', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '32', 'decimal_places': '28', 'blank': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.State']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_district_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_district_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.jslps_block': {
            'Meta': {'object_name': 'JSLPS_Block'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.Block']", 'null': 'True', 'blank': 'True'}),
            'block_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'block_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_jslps_block_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_jslps_block_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.jslps_district': {
            'Meta': {'object_name': 'JSLPS_District'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.District']", 'null': 'True', 'blank': 'True'}),
            'district_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_jslps_district_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_jslps_district_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.jslps_village': {
            'Meta': {'object_name': 'JSLPS_Village'},
            'Village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.Village']", 'null': 'True', 'blank': 'True'}),
            'block_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_jslps_village_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_jslps_village_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geographies.state': {
            'Meta': {'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_state_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_state_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.Block']"}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_village_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_village_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geographies']