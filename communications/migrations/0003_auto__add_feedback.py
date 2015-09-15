# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feedback'
        db.create_table(u'communications_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 9, 11, 0, 0))),
        ))
        db.send_create_signal(u'communications', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'Feedback'
        db.delete_table(u'communications_feedback')


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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 9, 11, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        }
    }

    complete_apps = ['communications']