# -*- coding: utf-8 -*-
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
                obj.type = "Error"
            else:
                data = minidom.parseString(obj.xml_data)
                if data.getElementsByTagName('data'):
                    type = data.getElementsByTagName('data')[0].attributes['name'].value
                    if type.lower() == 'screening form' or type.lower() == 'screening':
                        type= "Screening"
                    elif type.lower() == 'adoption form' or type.lower() == 'adoption':
                        type= "Adoption"
                    obj.type = type
                elif data.getElementsByTagName('device_report'):
                    obj.type = "Report"
            obj.save()
        
    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'dimagi.xmlsubmission': {
            'Meta': {'object_name': 'XMLSubmission'},
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
