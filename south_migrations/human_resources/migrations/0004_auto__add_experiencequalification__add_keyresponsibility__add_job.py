# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExperienceQualification'
        db.create_table('human_resources_experiencequalification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['human_resources.Job'])),
            ('point', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('human_resources', ['ExperienceQualification'])

        # Adding model 'KeyResponsibility'
        db.create_table('human_resources_keyresponsibility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['human_resources.Job'])),
            ('point', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('human_resources', ['KeyResponsibility'])

        # Adding model 'Job'
        db.create_table('human_resources_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('conclusion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('human_resources', ['Job'])


    def backwards(self, orm):
        # Deleting model 'ExperienceQualification'
        db.delete_table('human_resources_experiencequalification')

        # Deleting model 'KeyResponsibility'
        db.delete_table('human_resources_keyresponsibility')

        # Deleting model 'Job'
        db.delete_table('human_resources_job')


    models = {
        'human_resources.experiencequalification': {
            'Meta': {'object_name': 'ExperienceQualification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['human_resources.Job']"}),
            'point': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'human_resources.job': {
            'Meta': {'object_name': 'Job'},
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
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