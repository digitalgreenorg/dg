# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from xml.dom import minidom
from communications.models import Article
from time import strptime
import unicodedata

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        xmldoc = minidom.parse('C:\Users\chandu\Documents\dg\dg\media\Output\press.xml')
        itemlist = xmldoc.getElementsByTagName('TEAM')
        for item in itemlist:
            source = item.getElementsByTagName('TITLE')[0].childNodes[0].nodeValue
            title = item.getElementsByTagName('HEADLINE')[0].childNodes[0].nodeValue
            link = item.getElementsByTagName('REFERENCE')[0].childNodes[0].nodeValue
            pub_date = item.getElementsByTagName('PRESSDATE')[0].childNodes[0].nodeValue
            str = pub_date.split(', ', 1)[1]
            format=str.split(' ')
            day = format[0]
            month=format[1]
            year=format[2]            
            month_no1=strptime(month, '%b').tm_mon
            year1 = unicodedata.normalize('NFKD', year).encode('ascii','ignore')
            day1 = unicodedata.normalize('NFKD', day).encode('ascii','ignore')            
            pub_date2="%s-%s-%s" % (year1,unicode(month_no1),day1)            
            content = item.getElementsByTagName('DESC')[0].childNodes[0].nodeValue
            article = Article(title=title,pub_date=pub_date2,source=source,location=location,content=content,link=link)
            article.save()
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'communications.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pub_date': ('django.db.models.fields.DateField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }
    
    complete_apps = ['communications']
    symmetrical = True
