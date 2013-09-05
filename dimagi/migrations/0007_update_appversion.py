# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from xml.dom import minidom

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        objs = orm['dimagi.XMLSubmission'].objects.all()
        for obj in objs:
            if obj.xml_data== '':
                obj.app_version = 0
            else:
                data = minidom.parseString(obj.xml_data)
                if data.getElementsByTagName('data'):
                    version = int(data.getElementsByTagName('data')[0].attributes['version'].value)
                    obj.app_version = version
                    
                    obj.username = str(data.getElementsByTagName('n0:username')[0].childNodes[0].nodeValue)
                    
                    start = data.getElementsByTagName('n0:timeStart')[0].childNodes[0].nodeValue.split('T')
                    start_date = str(start[0])
                    start_time = str(start[1].split('.')[0])
                    obj.start_time = start_date+" "+start_time
                    
                    end = data.getElementsByTagName('n0:timeEnd')[0].childNodes[0].nodeValue.split('T')
                    end_date = str(end[0])
                    end_time = str(end[1].split('.')[0])
                    obj.end_time = end_date+" "+end_time
                    
                elif data.getElementsByTagName('device_report'):
                    obj.app_version = 0
            obj.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'dimagi.xmlsubmission': {
            'Meta': {'object_name': 'XMLSubmission'},
            'app_version': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'submission_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'username': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'xml_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dimagi']
    symmetrical = True
