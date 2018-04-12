# -*- coding: utf-8 -*-
import datetime, os
from dg.base_settings import PROJECT_PATH
from human_resources.models import Member, team_choices
from django.db import models
from south.db import db
from south.v2 import DataMigration
from xml.dom import minidom

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."        
        xmldoc = minidom.parse(os.path.join(PROJECT_PATH, 'media/Output/team_members.xml'))        
        itemlist = xmldoc.getElementsByTagName('TEAM')
        for item in itemlist:
            name = item.getElementsByTagName('NAME')[0].childNodes[0].nodeValue
            designation = item.getElementsByTagName('TITLE')[0].childNodes[0].nodeValue
            image = item.getElementsByTagName('ARTIST')[0].childNodes[0].nodeValue
            personal_intro = item.getElementsByTagName('DESC')[0].childNodes[0].nodeValue
            email = item.getElementsByTagName('MAILID')[0].childNodes[0].nodeValue
            team = "Program Team"
            location = "Headquarters-Delhi"
            member = Member(designation=designation, image=image, personal_intro=personal_intro, email=email, name=name,team=team, location=location)
            member.save()
        
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        
    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'human_resources.member': {
            'Meta': {'object_name': 'Member'},
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
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
