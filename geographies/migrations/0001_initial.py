# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'geographies_country', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_country_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_country_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_coco_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('country_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['Country'])

        # Adding model 'Region'
        db.create_table(u'geographies_region', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_region_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_region_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_coco_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('region_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['Region'])

        # Adding model 'State'
        db.create_table(u'geographies_state', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_state_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_state_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_coco_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('state_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.Region'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.Country'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['State'])

        # Adding model 'District'
        db.create_table(u'geographies_district', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_district_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_district_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_coco_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('district_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.State'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programmes.Partner'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=31, decimal_places=28, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=32, decimal_places=28, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['District'])

        # Adding model 'Block'
        db.create_table(u'geographies_block', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_block_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_block_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_coco_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('block_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.District'])),
        ))
        db.send_create_signal(u'geographies', ['Block'])

        # Adding model 'Village'
        db.create_table(u'geographies_village', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_village_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'geographies_village_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_coco_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('village_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geographies.Block'])),
            ('no_of_households', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('population', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('road_connectivity', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('control', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal(u'geographies', ['Village'])

        # Adding unique constraint on 'Village', fields ['village_name', 'block']
        db.create_unique(u'geographies_village', ['village_name', 'block_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Village', fields ['village_name', 'block']
        db.delete_unique(u'geographies_village', ['village_name', 'block_id'])

        # Deleting model 'Country'
        db.delete_table(u'geographies_country')

        # Deleting model 'Region'
        db.delete_table(u'geographies_region')

        # Deleting model 'State'
        db.delete_table(u'geographies_state')

        # Deleting model 'District'
        db.delete_table(u'geographies_district')

        # Deleting model 'Block'
        db.delete_table(u'geographies_block')

        # Deleting model 'Village'
        db.delete_table(u'geographies_village')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {}),
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
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {}),
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
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['programmes.Partner']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.State']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_district_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_district_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_region_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_region_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'geographies.state': {
            'Meta': {'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geographies.Region']"}),
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
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'no_of_households': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'road_connectivity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_village_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'geographies_village_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'programmes.partner': {
            'Meta': {'object_name': 'Partner'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'date_of_association': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_coco_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'programmes_partner_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'programmes_partner_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['geographies']