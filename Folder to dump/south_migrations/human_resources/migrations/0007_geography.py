# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        description = 'Digital Green is an international, non-profit development organization that builds and deploys information and communication technology to amplify the effectiveness of development efforts to affect sustained, social change. The Digital Green approach combines technology and social organization to improve the cost-effectiveness of extension systems globally, and broaden the community participation in existing best practices. The organization is supported by Bill and Melinda Gates Foundation, Department for International Development, the Government of India, Ford Foundation, Vodafone Foundation and others. Digital Green’s primary head office is located in New Delhi. Considering Digital Green is expanding its work rapidly in Sub-Saharan Africa, the organization is creating a country office in Ethiopia. Digital Green is currently working with Ethiopia’s Ministry of Agriculture and other NGO partners in the country, such as Oxfam America, Sasakawa Africa Association, and International Development Enterprises. Within the next few years, Digital Green will increase its scale significantly in the country.'
        Geography = orm['human_resources.Geography']
        geography = Geography(name="Ethiopia", description=description, hierarchy_number=1.0)
        geography.save()
    
    def backwards(self, orm):
        "Write your backwards methods here."

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
    symmetrical = True
