# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'loop_country', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_country_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_country_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'loop', ['Country'])

        # Adding unique constraint on 'Country', fields ['country_name']
        db.create_unique(u'loop_country', ['country_name'])

        # Adding model 'State'
        db.create_table(u'loop_state', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_state_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_state_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.Country'])),
        ))
        db.send_create_signal(u'loop', ['State'])

        # Adding unique constraint on 'State', fields ['state_name']
        db.create_unique(u'loop_state', ['state_name'])

        # Adding model 'District'
        db.create_table(u'loop_district', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_district_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_district_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.State'])),
        ))
        db.send_create_signal(u'loop', ['District'])

        # Adding unique constraint on 'District', fields ['district_name', 'state']
        db.create_unique(u'loop_district', ['district_name', 'state_id'])

        # Adding model 'Block'
        db.create_table(u'loop_block', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_block_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_block_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.District'])),
        ))
        db.send_create_signal(u'loop', ['Block'])

        # Adding unique constraint on 'Block', fields ['block_name', 'district']
        db.create_unique(u'loop_block', ['block_name', 'district_id'])

        # Adding model 'Village'
        db.create_table(u'loop_village', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_village_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_village_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('village_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.Block'])),
        ))
        db.send_create_signal(u'loop', ['Village'])

        # Adding unique constraint on 'Village', fields ['village_name', 'block']
        db.create_unique(u'loop_village', ['village_name', 'block_id'])

        # Adding model 'LoopUser'
        db.create_table(u'loop_loopuser', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_loopuser_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_loopuser_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='loop_user', unique=True, to=orm['auth.User'])),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
            ('mode', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(default='0', max_length=14)),
        ))
        db.send_create_signal(u'loop', ['LoopUser'])

        # Adding M2M table for field assigned_villages on 'LoopUser'
        m2m_table_name = db.shorten_name(u'loop_loopuser_assigned_villages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('loopuser', models.ForeignKey(orm[u'loop.loopuser'], null=False)),
            ('village', models.ForeignKey(orm[u'loop.village'], null=False))
        ))
        db.create_unique(m2m_table_name, ['loopuser_id', 'village_id'])

        # Adding model 'Farmer'
        db.create_table(u'loop_farmer', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_farmer_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_farmer_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('image_path', self.gf('django.db.models.fields.CharField')(default=None, max_length=500, null=True, blank=True)),
            ('village', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.Village'])),
        ))
        db.send_create_signal(u'loop', ['Farmer'])

        # Adding unique constraint on 'Farmer', fields ['phone', 'name']
        db.create_unique(u'loop_farmer', ['phone', 'name'])

        # Adding model 'Crop'
        db.create_table(u'loop_crop', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_crop_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_crop_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_path', self.gf('django.db.models.fields.CharField')(default=None, max_length=500, null=True, blank=True)),
            ('crop_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('measuring_unit', self.gf('django.db.models.fields.CharField')(default='kg', max_length=20)),
        ))
        db.send_create_signal(u'loop', ['Crop'])

        # Adding unique constraint on 'Crop', fields ['crop_name']
        db.create_unique(u'loop_crop', ['crop_name'])

        # Adding model 'Mandi'
        db.create_table(u'loop_mandi', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_mandi_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_mandi_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mandi_name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.District'])),
        ))
        db.send_create_signal(u'loop', ['Mandi'])

        # Adding unique constraint on 'Mandi', fields ['mandi_name', 'district']
        db.create_unique(u'loop_mandi', ['mandi_name', 'district_id'])

        # Adding model 'CombinedTransaction'
        db.create_table(u'loop_combinedtransaction', (
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_combinedtransaction_created', null=True, to=orm['auth.User'])),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'loop_combinedtransaction_related_modified', null=True, to=orm['auth.User'])),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('farmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.Farmer'])),
            ('crop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.Crop'])),
            ('mandi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loop.Mandi'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'loop', ['CombinedTransaction'])

        # Adding unique constraint on 'CombinedTransaction', fields ['date', 'farmer', 'crop', 'mandi', 'price']
        db.create_unique(u'loop_combinedtransaction', ['date', 'farmer_id', 'crop_id', 'mandi_id', 'price'])

        # Adding model 'Log'
        db.create_table(u'loop_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('village', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('action', self.gf('django.db.models.fields.IntegerField')()),
            ('entry_table', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('model_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'loop', ['Log'])


    def backwards(self, orm):
        # Removing unique constraint on 'CombinedTransaction', fields ['date', 'farmer', 'crop', 'mandi', 'price']
        db.delete_unique(u'loop_combinedtransaction', ['date', 'farmer_id', 'crop_id', 'mandi_id', 'price'])

        # Removing unique constraint on 'Mandi', fields ['mandi_name', 'district']
        db.delete_unique(u'loop_mandi', ['mandi_name', 'district_id'])

        # Removing unique constraint on 'Crop', fields ['crop_name']
        db.delete_unique(u'loop_crop', ['crop_name'])

        # Removing unique constraint on 'Farmer', fields ['phone', 'name']
        db.delete_unique(u'loop_farmer', ['phone', 'name'])

        # Removing unique constraint on 'Village', fields ['village_name', 'block']
        db.delete_unique(u'loop_village', ['village_name', 'block_id'])

        # Removing unique constraint on 'Block', fields ['block_name', 'district']
        db.delete_unique(u'loop_block', ['block_name', 'district_id'])

        # Removing unique constraint on 'District', fields ['district_name', 'state']
        db.delete_unique(u'loop_district', ['district_name', 'state_id'])

        # Removing unique constraint on 'State', fields ['state_name']
        db.delete_unique(u'loop_state', ['state_name'])

        # Removing unique constraint on 'Country', fields ['country_name']
        db.delete_unique(u'loop_country', ['country_name'])

        # Deleting model 'Country'
        db.delete_table(u'loop_country')

        # Deleting model 'State'
        db.delete_table(u'loop_state')

        # Deleting model 'District'
        db.delete_table(u'loop_district')

        # Deleting model 'Block'
        db.delete_table(u'loop_block')

        # Deleting model 'Village'
        db.delete_table(u'loop_village')

        # Deleting model 'LoopUser'
        db.delete_table(u'loop_loopuser')

        # Removing M2M table for field assigned_villages on 'LoopUser'
        db.delete_table(db.shorten_name(u'loop_loopuser_assigned_villages'))

        # Deleting model 'Farmer'
        db.delete_table(u'loop_farmer')

        # Deleting model 'Crop'
        db.delete_table(u'loop_crop')

        # Deleting model 'Mandi'
        db.delete_table(u'loop_mandi')

        # Deleting model 'CombinedTransaction'
        db.delete_table(u'loop_combinedtransaction')

        # Deleting model 'Log'
        db.delete_table(u'loop_log')


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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_block_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_block_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.combinedtransaction': {
            'Meta': {'unique_together': "(('date', 'farmer', 'crop', 'mandi', 'price'),)", 'object_name': 'CombinedTransaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'crop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Crop']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Farmer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandi': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Mandi']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_combinedtransaction_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_combinedtransaction_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.country': {
            'Meta': {'unique_together': "(('country_name',),)", 'object_name': 'Country'},
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'measuring_unit': ('django.db.models.fields.CharField', [], {'default': "'kg'", 'max_length': '20'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_crop_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_crop_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.district': {
            'Meta': {'unique_together': "(('district_name', 'state'),)", 'object_name': 'District'},
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_farmer_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_farmer_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Village']"})
        },
        u'loop.log': {
            'Meta': {'object_name': 'Log'},
            'action': ('django.db.models.fields.IntegerField', [], {}),
            'entry_table': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'village': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'loop.loopuser': {
            'Meta': {'object_name': 'LoopUser'},
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_villages'", 'symmetrical': 'False', 'to': u"orm['loop.Village']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '14'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'loop_user'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuser_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_loopuser_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.mandi': {
            'Meta': {'unique_together': "(('mandi_name', 'district'),)", 'object_name': 'Mandi'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'state_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_state_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'loop_state_related_modified'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'loop.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loop.Block']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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