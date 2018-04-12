# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Member.location'
        db.delete_column('human_resources_member', 'location')


    def backwards(self, orm):
        # Adding field 'Member.location'
        db.add_column('human_resources_member', 'location',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


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
            'Meta': {'ordering': "['-geography__hierarchy_number', 'geography__name', '-hierarchy_num', 'title']", 'object_name': 'Job'},
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geography': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['human_resources.Geography']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_intro': ('django.db.models.fields.TextField', [], {}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['human_resources.Place']", 'null': 'True'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'human_resources.place': {
            'Meta': {'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['human_resources']