# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Feedback.time'
        db.add_column(u'communications_feedback', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Feedback.time'
        db.delete_column(u'communications_feedback', 'time')


    models = {
        u'communications.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pub_date': ('django.db.models.fields.DateField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'communications.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 11, 16, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        }
    }

    complete_apps = ['communications']