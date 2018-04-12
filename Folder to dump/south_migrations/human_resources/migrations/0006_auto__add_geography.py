# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Geography'
        db.create_table('human_resources_geography', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('hierarchy_number', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('human_resources', ['Geography'])


    def backwards(self, orm):
        # Deleting model 'Geography'
        db.delete_table('human_resources_geography')


    models = {
        'human_resources.experiencequalification': {
            'Meta': {'object_name': 'ExperienceQualification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['human_resources.Job']"}),
            'point': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'human_resources.geography': {
            'Meta': {'object_name': 'Geography'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'hierarchy_number': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'human_resources.job': {
            'Meta': {'object_name': 'Job'},
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hierarchy_num': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'human_resources.keyresponsibility': {
            'Meta': {'object_name': 'KeyResponsibility'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['human_resources.Job']"}),
            'point': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'human_resources.member': {
            'Meta': {'object_name': 'Member'},
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'hierarchy_num': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_intro': ('django.db.models.fields.TextField', [], {}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['human_resources']