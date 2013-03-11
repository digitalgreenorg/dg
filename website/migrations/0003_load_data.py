# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db.models import Sum, Count, Q
from website.models import *
import gdata.youtube.service

class Migration(DataMigration):

    def farmer_migration(self, orm, i):
        if i.group!=None:
                group_name=i.group.group_name
        else:
            group_name=''
        partner=Partner.objects.get(uid=str(i.village.block.district.partner.id))
        temp=Farmer(uid=str(i.id),name=i.person_name,thumbnailURL="https://s3.amazonaws.com/dg_farmerbook/2/"+str(i.id)+".jpg",village=i.village.village_name,block=i.village.block.block_name,district=i.village.block.district.district_name,state=i.village.block.district.state.state_name,country=i.village.block.district.state.country.country_name,group=group_name,partner=partner)
        temp.save()
        videos = orm['dashboard.PersonMeetingAttendance'].objects.filter(person_id=int(i.id)).values_list('screening__videoes_screened')
        collection=[]
        for j in videos:
            if(len(Video.objects.filter(uid=j))==1):
                collection.extend(list(Collection.objects.filter(videos=j)))
        for j in set(collection):
            temp.collections.add(j)
        
    def forwards(self, orm):
#        country migrations

        country=orm['dashboard.Country'].objects.all()
        for j in country:
            temp=Country(countryName=j.country_name)
            temp.save()

#        language migrations

        lang=orm['dashboard.Language'].objects.all()
        for i in lang:
            temp=Language(name=i.language_name)
            temp.save()

#        partner migrations basic

        partner = orm['dashboard.Partners'].objects.exclude(date_of_association=None)
        for i in partner:
            temp = Partner(uid=str(i.id),joinDate=i.date_of_association,name=i.partner_name,description=i.description,logoURL=i.logoURL,collectionCount = 0,videos = 0, views = 0,likes = 0, adoptions = 0)
            temp.save()

#        video migrations

        yt_service = gdata.youtube.service.YouTubeService()
        yt_service.developer_key = 'AI39si74a5fwzrBsgSxjgImSsImXHfGgt8IpozLxty9oGP7CH0ky4Hf1eetV10IBi2KlgcgkAX-vmtmG86fdAX2PaG2CQPtkpA'
        yt_service.ssl = False
        video=orm['dashboard.Video'].objects.all()
        for i in video:
            offlk=0
            offvw=0
            sec=""
            subsec=""
            top=""
            subtop=""
            sub=""
            partner=Partner.objects.get(uid=str(i.village.block.district.partner.id))
            lang=Language.objects.get(name=str(i.language.language_name))
            if (i.related_practice != None):
                if i.related_practice.practice_sector != None:
                    sec=i.related_practice.practice_sector.name
                if i.related_practice.practice_subsector != None:
                    subsec=i.related_practice.practice_subsector.name
                if i.related_practice.practice_topic != None:
                    top=i.related_practice.practice_topic.name
                if i.related_practice.practice_subtopic != None:
                    subtop=i.related_practice.practice_subtopic.name
                if i.related_practice.practice_subject != None:
                    sub=i.related_practice.practice_subject.name

            for j in orm['dashboard.VideosScreenedInScreening'].objects.filter(video_id=i.id):
                offvw = offvw + len(orm['dashboard.PersonMeetingAttendance'].objects.filter(screening_id = j.screening_id))
                offlk = offlk + int(orm['dashboard.PersonMeetingAttendance'].objects.filter(screening_id = 6000019734).values ('screening_id').annotate(count = Sum('interested')).values_list('count', flat=True)[0])
            adops=len(orm['dashboard.PersonAdoptPractice'].objects.filter(video_id=i.id))
            if i.youtubeid!="":
                try:
                    entry = yt_service.GetYouTubeVideoEntry(video_id=i.youtubeid)
                    if entry.rating is not None:
                        temp=Video(uid=str(i.id), title=i.title, thumbnailURL=entry.media.thumbnail[0].url, description=i.summary, youtubeID=i.youtubeid, duration=int(entry.media.duration.seconds), date=i.video_production_end_date, onlineLikes=int((float(entry.rating.average)*float(entry.rating.num_raters)-float(entry.rating.num_raters))/4), offlineLikes=offlk, onlineViews=int(entry.statistics.view_count), offlineViews=offvw, adoptions=adops, sector=sec, subsector=subsec, topic=top, subtopic=subtop, subject=sub, partner=partner, language=lang, state = i.village.block.district.state.state_name)
                        temp.save()
                    else:
                        temp=Video(uid=str(i.id), title=i.title, thumbnailURL=entry.media.thumbnail[0].url, description=i.summary, youtubeID=i.youtubeid, duration=int(entry.media.duration.seconds), date=i.video_production_end_date, onlineLikes=0, offlineLikes=offlk, onlineViews=int(entry.statistics.view_count), offlineViews=offvw, adoptions=adops, sector=sec, subsector=subsec, topic=top, subtopic=subtop, subject=sub, partner=partner, language=lang, state = i.village.block.district.state.state_name)
                        temp.save()
                except Exception, ex:
                    temp=Video(uid=str(i.id), title=i.title, description=i.summary, date=i.video_production_end_date, onlineLikes=0, offlineLikes=offlk, onlineViews=0, offlineViews=offvw, adoptions=adops, sector=sec, subsector=subsec, topic=top, subtopic=subtop, subject=sub, partner=partner, language=lang, state = i.village.block.district.state.state_name)
                    temp.save()
                    print ex
                    pass
            else:
                temp=Video(uid=str(i.id), title=i.title, description=i.summary, date=i.video_production_end_date, onlineLikes=0, offlineLikes=offlk, onlineViews=0, offlineViews=offvw, adoptions=adops, sector=sec, subsector=subsec, topic=top, subtopic=subtop, subject=sub, partner=partner, language=lang, state = i.village.block.district.state.state_name)
                temp.save()
                
#            collections migrations

        collection_comb = Video.objects.exclude(topic="").values_list('partner_id','language__name','topic','state').annotate(c= Count('uid')).filter(c__gte=5,c__lte=25)
        counter = 1
        for i in collection_comb:
            partner=i[0]
            lang=i[1]
            topic=i[2]
            state=i[3]
            country=Country.objects.get(countryName=str(orm['dashboard.Partners'].objects.get(id=int(partner)).district_set.all()[0].state.country.country_name))
            videos = Video.objects.filter(partner_id=partner,language__name=lang,topic = topic, state=state)
            if len(set(videos.values_list('sector')))==1 and videos[0].sector!= "":
                sector = videos[0].sector
            else:
                sector = ""
            if len(set(videos.values_list('subsector')))==1 and videos[0].subsector!= "":
                subsector = videos[0].subsector
            else:
                subsector = ""
            if len(set(videos.values_list('subject')))==1 and videos[0].subject != "":
                subject = videos[0].subject
            else:
                subject = ""
            if len(set(videos.values_list('subtopic')))==1 and videos[0].subtopic != "":
                subtopic = videos[0].subtopic
            else:
                subtopic = ""
            temp = Collection(uid=str(counter), title=videos[0].topic, thumbnailURL=videos[0].thumbnailURL, state=state, country=country, partner=Partner.objects.get(uid=partner), language=Language.objects.get(name=lang), category=sector, subcategory=subsector, topic=videos[0].topic, subtopic=subtopic,  subject=subject)
            temp.save()
            part= Partner.objects.get(uid=partner)
            count=part.collectionCount
            part.collectionCount=(count+1)
            part.save()
            for vid in videos:
                temp.videos.add(vid)
            counter = counter+1
            
        collection_comb = Video.objects.exclude(subject="").values_list('partner_id','language__name','subject','state').annotate(c= Count('uid')).filter(c__gte=5,c__lte=25)
        for i in collection_comb:
            partner=i[0]
            lang=i[1]
            sub=i[2]
            state=i[3]
            country=Country.objects.get(countryName=str(orm['dashboard.Partners'].objects.get(id=int(partner)).district_set.all()[0].state.country.country_name))
            videos = Video.objects.filter(partner__uid=partner,language__name=lang,subject = sub, state=state)
            if len(set(videos.values_list('sector')))==1 and videos[0].sector!= "":
                sector = videos[0].sector
            else:
                sector = ""
            if len(set(videos.values_list('subsector')))==1 and videos[0].subsector!= "":
                subsector = videos[0].subsector
            else:
                subsector = ""
            if len(set(videos.values_list('topic')))==1 and videos[0].topic != "":
                continue
            else:
                topic = ""
            if len(set(videos.values_list('subtopic')))==1 and videos[0].subtopic != "":
                subtopic = videos[0].subtopic
            else:
                subtopic = ""
            temp = Collection(uid=str(counter), title=videos[0].subject, thumbnailURL=videos[0].thumbnailURL, state=state, country=country, partner=Partner.objects.get(uid=partner), language=Language.objects.get(name=lang), category=sector, subcategory=subsector, topic=topic, subtopic=subtopic,  subject=videos[0].subject)
            temp.save()
            part= Partner.objects.get(uid=partner)
            count=part.collectionCount
            part.collectionCount=(count+1)
            part.save()
            for vid in videos:
                temp.videos.add(vid)
            counter = counter+1
            
#        partner migrations statistics

        partner = Partner.objects.all()
        for i in partner:
            stats = Video.objects.filter(partner_id=i.uid).aggregate(videos = Sum('uid'), onlineLikes = Sum('onlineLikes'), offlineLikes = Sum('offlineLikes'), onlineViews = Sum('onlineViews'), offlineViews = Sum('offlineViews'), adoptions = Sum('adoptions'))
            if stats['videos']!=None:
                i.videos = stats['videos']
                i.likes = stats['onlineLikes'] + stats['offlineLikes']
                i.views = stats['onlineViews'] + stats['offlineViews']
                i.adoptions = stats['adoptions']
                i.save()


#        farmer migrations

        for j in orm['dashboard.Partner'].objects.exclude(date_of_association=None):
            farmer=orm['dashboard.Person'].objects.filter(village__block__district__partner=j).exclude(image_exists=False)[:100]
            for i in farmer:
                self.farmer_migration(orm, i);
            
        #interest migrations
        subject=orm['dashboard.PracticeSubject'].objects.all()
        for i in range(len(subject)):
            temp=Interests(uid=str(i+1),name=subject[i].name)
            temp.save()
            pap = orm['dashboard.PersonAdoptPractice'].objects.filter(video__related_practice__practice_subject_id=subject[i].id)
            for j in pap:
                if len(Farmer.objects.filter(uid=str(j.person_id)))==1:
                    farmer = Farmer.objects.get(uid=str(j.person_id))
                    farmer.interests.add(temp)
            
            
#        activity migrations
#
#        farmer=Farmer.objects.all()
#        activity=[]
#        for i in farmer:
#            person=orm['dashboard.Person'].objects.get(id=int(i.uid))
#            videos_watched=orm['dashboard.PersonMeetingAttendance'].objects.filter(person_id = person.id).values_list('screening__videoes_screened__title', 'screening__date','screening__videoes_screened__id').order_by('screening__date')
#            videos_adopted=orm['dashboard.PersonAdoptPractice'].objects.filter(person_id = person.id).values_list('video__title', 'date_of_adoption','video_id').order_by('date_of_adoption')
#            person_activity=[]
#            vw=va=0
#            for j in range(len(videos_watched)+len(videos_adopted)):
#                if(vw==len(videos_watched)):
#                    if len(Video.objects.filter(uid=str(videos_adopted[va][2])))==1:
#                        temp=[i,videos_adopted[va][0],videos_adopted[va][1],'A',videos_adopted[va][2]]
#                        person_activity.append(temp)
#                    va=va+1
#                elif (va==len(videos_adopted)):
#                    if len(Video.objects.filter(uid=str(videos_watched[vw][2])))==1:
#                        temp=[i,videos_watched[vw][0],videos_watched[vw][1],'S',videos_watched[vw][2]]
#                        person_activity.append(temp)
#                    vw=vw+1
#                elif(videos_watched[vw][1]<videos_adopted[va][1]):
#                    if len(Video.objects.filter(uid=str(videos_watched[vw][2])))==1:
#                        temp=[i,videos_watched[vw][0],videos_watched[vw][1],'S',videos_watched[vw][2]]
#                        person_activity.append(temp)
#                    vw=vw+1
#                else:
#                    if len(Video.objects.filter(uid=str(videos_adopted[va][2])))==1:
#                        temp=[i,videos_adopted[va][0],videos_adopted[va][1],'A',videos_adopted[va][2]]
#                        person_activity.append(temp)
#                    va=va+1
#            activity.append(person_activity)
#        counter=1
#        for i in range(len(activity)):
#            for j in range(len(activity[i])):
#                if(activity[i][j][3]=='S'):
#                    temp = Activity(uid=str(counter),date=activity[i][j][2],textContent="Today "+activity[i][j][0].name+" saw video titled "+ activity[i][j][1],video=Video.objects.get(uid=str(activity[i][j][4])),farmer=activity[i][j][0])
#                    temp.save()
#                    counter=counter+1
#                else:
#                    temp=Activity(uid=str(counter),date=activity[i][j][2],textContent="Today "+activity[i][j][0].name+" adopted video titled "+ activity[i][j][1],video=Video.objects.get(uid=str(activity[i][j][4])),farmer=activity[i][j][0])
#                    temp.save()
#                    counter=counter+1
        
        partner=orm['dashboard.Partners'].objects.exclude(date_of_association=None).order_by('date_of_association')
        #template_partner_expansion = "Our Partner %s has expanded their work to reach %n villages today"
        #textContent = template_partner_expansion % (i.partner_name, 10)
        for i in partner:
            repeat_flag=False
            partner_village_count=0
            last_date=datetime.date.today()
            district = i.district_set.all().order_by('start_date')
            for j in district:
                block = j.block_set.all().order_by('start_date')
                for k in block:
                    village = k.village_set.all().order_by('start_date')
                    for l in village:
                        if partner_village_count==10 and repeat_flag==False:
                            temp = Activity(uid=str(counter),date=last_date,textContent="Our Partner "+i.partner_name+" has expanded their work to reach 10 villages today",partner=Partner.objects.get(uid=i.id), video = Video.objects.all()[0])
                            temp.save()
                            counter = counter + 1
                            repeat_flag=True
                        if partner_village_count==50 and repeat_flag==False:
                            temp = Activity(uid=str(counter), date=last_date, textContent="Our Partner organisation "+i.partner_name+" have expanded there work in 50 villages today", partner=Partner.objects.get(uid=i.id), video = Video.objects.all()[0])
                            temp.save()
                            counter = counter + 1
                            repeat_flag=True
                        if partner_village_count==100 and repeat_flag==False:
                            temp = Activity(uid=str(counter), date=last_date, textContent="Our Partner organisation "+i.partner_name+" have expanded there work in 100 villages today", partner=Partner.objects.get(uid=i.id), video = Video.objects.all()[0])
                            temp.save()
                            counter = counter + 1
                            repeat_flag=True
                        if l.start_date is None:
                            continue
                        else:
                            last_date = l.start_date
                        temp = Activity(uid=str(counter), date=last_date, textContent="Our Partner organisation "+i.partner_name+" started working in Village "+l.village_name+" today", partner=Partner.objects.get(uid=i.id), video = Video.objects.all()[0])
                        temp.save()
                        counter = counter + 1
                        partner_village_count = partner_village_count + 1
                        repeat_flag=False
                        video = l.video_set.all().order_by('video_production_end_date')
                        for m in video:
                            if len(Video.objects.filter(uid=str(m.id)))==1:
                                temp = Activity(uid=str(counter),date=m.video_production_end_date, textContent="A new video titled "+m.title+" was produced by our Partner "+i.partner_name, partner = Partner.objects.get(uid=i.id), video = Video.objects.get(uid=str(m.id)))
                                temp.save()
                                counter = counter + 1                
       
#        comment migrations
        farmer=Farmer.objects.all()
        counter=1
        for i in farmer:
            pmas = orm['dashboard.PersonMeetingAttendance'].objects.filter(person_id=int(i.uid))
            for j in pmas:
                if j.expressed_question!='':
                    for k in j.screening.videoes_screened.all():
                        if len(Video.objects.filter(uid=str(k.id)))==1:
                            temp=Comment(uid=str(counter),date=j.screening.date,text=j.expressed_question,isOnline=False,farmer=i,video =Video.objects.get(uid=str(k.id)) )
                            temp.save()
            
            
    def backwards(self, orm):
        pass
        "Write your backwards methods here."
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.animator': {
            'Meta': {'unique_together': "(('name', 'gender', 'partner', 'village'),)", 'object_name': 'Animator', 'db_table': "u'ANIMATOR'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_villages'", 'to': "orm['dashboard.Village']", 'through': "orm['dashboard.AnimatorAssignedVillage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'camera_operator_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CAMERA_OPERATOR_FLAG'", 'blank': 'True'}),
            'csp_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CSP_FLAG'", 'blank': 'True'}),
            'facilitator_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'FACILITATOR_FLAG'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'total_adoptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'db_column': "'home_village_id'"})
        },
        'dashboard.animatorassignedvillage': {
            'Meta': {'object_name': 'AnimatorAssignedVillage', 'db_table': "u'ANIMATOR_ASSIGNED_VILLAGE'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.animatorsalarypermonth': {
            'Meta': {'object_name': 'AnimatorSalaryPerMonth', 'db_table': "u'ANIMATOR_SALARY_PER_MONTH'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'pay_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PAY_DATE'", 'blank': 'True'}),
            'total_salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_SALARY'", 'blank': 'True'})
        },
        'dashboard.block': {
            'Meta': {'object_name': 'Block', 'db_table': "u'BLOCK'"},
            'block_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'BLOCK_NAME'"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'COUNTRY'"},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'COUNTRY_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.developmentmanager': {
            'Meta': {'object_name': 'DevelopmentManager', 'db_table': "u'DEVELOPMENT_MANAGER'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'}),
            'speciality': ('django.db.models.fields.TextField', [], {'db_column': "'SPECIALITY'", 'blank': 'True'}),
            'start_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DAY'", 'blank': 'True'})
        },
        'dashboard.district': {
            'Meta': {'object_name': 'District', 'db_table': "u'DISTRICT'"},
            'district_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'DISTRICT_NAME'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']"}),
            'fieldofficer_startday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'FIELDOFFICER_STARTDAY'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.State']"})
        },
        'dashboard.equipment': {
            'Meta': {'object_name': 'Equipment', 'db_table': "u'EQUIPMENT_ID'"},
            'additional_accessories': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COST'", 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.IntegerField', [], {'db_column': "'EQUIPMENT_TYPE'"}),
            'equipmentholder': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.EquipmentHolder']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'installation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'INVOICE_NO'"}),
            'is_reserve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'MODEL_NO'", 'blank': 'True'}),
            'other_equipment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'db_column': "'OTHER_EQUIPMENT'", 'blank': 'True'}),
            'procurement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PROCUREMENT_DATE'", 'blank': 'True'}),
            'purpose': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'purpose'", 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'SERIAL_NO'", 'blank': 'True'}),
            'transfer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'null': 'True', 'blank': 'True'}),
            'warranty_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'WARRANTY_EXPIRATION_DATE'", 'blank': 'True'})
        },
        'dashboard.equipmentholder': {
            'Meta': {'object_name': 'EquipmentHolder', 'db_table': "u'EQUIPMENT_HOLDER'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {})
        },
        'dashboard.error': {
            'Meta': {'unique_together': "(('rule', 'content_type1', 'object_id1', 'content_type2', 'object_id2'),)", 'object_name': 'Error'},
            'content_type1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type1'", 'to': "orm['contenttypes.ContentType']"}),
            'content_type2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type2'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notanerror': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id1': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'object_id2': ('dashboard.fields.PositiveBigIntegerField', [], {'null': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Rule']"})
        },
        'dashboard.fieldofficer': {
            'Meta': {'object_name': 'FieldOfficer', 'db_table': "u'FIELD_OFFICER'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'})
        },
        'dashboard.groupstargetedinscreening': {
            'Meta': {'object_name': 'GroupsTargetedInScreening', 'db_table': "u'SCREENING_farmer_groups_targeted'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'persongroups': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'db_column': "'persongroups_id'"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"})
        },
        'dashboard.language': {
            'Meta': {'object_name': 'Language', 'db_table': "u'LANGUAGE'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'})
        },
        'dashboard.monthlycostpervillage': {
            'Meta': {'object_name': 'MonthlyCostPerVillage', 'db_table': "u'MONTHLY_COST_PER_VILLAGE'"},
            'community_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COMMUNITY_COST'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'digitalgreen_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'DIGITALGREEN_COST'", 'blank': 'True'}),
            'equipment_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'EQUIPMENT_COST'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'labor_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LABOR_COST'", 'blank': 'True'}),
            'miscellaneous_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'MISCELLANEOUS_COST'", 'blank': 'True'}),
            'partners_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'PARTNERS_COST'", 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_COST'", 'blank': 'True'}),
            'transportation_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TRANSPORTATION_COST'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.offlineuser': {
            'Meta': {'object_name': 'OfflineUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline_pk_id': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.partners': {
            'Meta': {'object_name': 'Partners', 'db_table': "u'PARTNERS'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'date_of_association': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'DATE_OF_ASSOCIATION'", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'logoURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PARTNER_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'})
        },
        'dashboard.person': {
            'Meta': {'unique_together': "(('person_name', 'father_name', 'group', 'village'),)", 'object_name': 'Person', 'db_table': "u'PERSON'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'date_of_joining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'FATHER_NAME'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'group': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'image_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'land_holdings': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LAND_HOLDINGS'", 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PERSON_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rel'", 'to': "orm['dashboard.Person']", 'through': "orm['dashboard.PersonRelations']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personadoptpractice': {
            'Meta': {'unique_together': "(('person', 'video', 'date_of_adoption'),)", 'object_name': 'PersonAdoptPractice', 'db_table': "u'PERSON_ADOPT_PRACTICE'"},
            'date_of_adoption': ('django.db.models.fields.DateField', [], {'db_column': "'DATE_OF_ADOPTION'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'prior_adoption_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'PRIOR_ADOPTION_FLAG'", 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'QUALITY'", 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'QUANTITY'", 'blank': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'QUANTITY_UNIT'", 'blank': 'True'}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']"})
        },
        'dashboard.persongroups': {
            'Meta': {'unique_together': "(('group_name', 'village'),)", 'object_name': 'PersonGroups', 'db_table': "u'PERSON_GROUPS'"},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'DAYS'", 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'GROUP_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'TIME_UPDATED'", 'blank': 'True'}),
            'timings': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'TIMINGS'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personmeetingattendance': {
            'Meta': {'object_name': 'PersonMeetingAttendance', 'db_table': "u'PERSON_MEETING_ATTENDANCE'"},
            'expressed_adoption_video': ('dashboard.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_adoption_video'", 'null': 'True', 'db_column': "'EXPRESSED_ADOPTION_VIDEO'", 'to': "orm['dashboard.Video']"}),
            'expressed_question': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_QUESTION'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'interested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'INTERESTED'", 'db_index': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']"})
        },
        'dashboard.personrelations': {
            'Meta': {'object_name': 'PersonRelations', 'db_table': "u'PERSON_RELATIONS'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'related_name': "'person'", 'to': "orm['dashboard.Person']"}),
            'relative': ('dashboard.fields.BigForeignKey', [], {'related_name': "'relative'", 'to': "orm['dashboard.Person']"}),
            'type_of_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'TYPE_OF_RELATIONSHIP'"})
        },
        'dashboard.personshowninvideo': {
            'Meta': {'object_name': 'PersonShownInVideo', 'db_table': "u'VIDEO_farmers_shown'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']", 'db_column': "'person_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.practices': {
            'Meta': {'unique_together': "(('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject'),)", 'object_name': 'Practices', 'db_table': "u'PRACTICES'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'practice_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': "'True'", 'null': 'True', 'db_column': "'PRACTICE_NAME'"}),
            'practice_sector': ('dashboard.fields.BigForeignKey', [], {'default': '1', 'to': "orm['dashboard.PracticeSector']"}),
            'practice_subject': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubject']", 'null': 'True'}),
            'practice_subsector': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubSector']", 'null': 'True'}),
            'practice_subtopic': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubtopic']", 'null': 'True'}),
            'practice_topic': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeTopic']", 'null': 'True'}),
            'seasonality': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "'SEASONALITY'"}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'})
        },
        'dashboard.practicesector': {
            'Meta': {'object_name': 'PracticeSector', 'db_table': "u'practice_sector'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicesubject': {
            'Meta': {'object_name': 'PracticeSubject', 'db_table': "u'practice_subject'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicesubsector': {
            'Meta': {'object_name': 'PracticeSubSector', 'db_table': "u'practice_subsector'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicesubtopic': {
            'Meta': {'object_name': 'PracticeSubtopic', 'db_table': "u'practice_subtopic'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicetopic': {
            'Meta': {'object_name': 'PracticeTopic', 'db_table': "u'practice_topic'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'REGION'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.regiontest': {
            'Meta': {'object_name': 'RegionTest', 'db_table': "u'REGION_TEST'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.reviewer': {
            'Meta': {'object_name': 'Reviewer', 'db_table': "u'REVIEWER'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {})
        },
        'dashboard.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_msg': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.screening': {
            'Meta': {'unique_together': "(('date', 'start_time', 'end_time', 'location', 'village'),)", 'object_name': 'Screening', 'db_table': "u'SCREENING'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'db_column': "'END_TIME'"}),
            'farmer_groups_targeted': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.PersonGroups']", 'symmetrical': 'False'}),
            'farmers_attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Person']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'LOCATION'", 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'db_column': "'START_TIME'"}),
            'target_adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_ADOPTIONS'", 'blank': 'True'}),
            'target_audience_interest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_AUDIENCE_INTEREST'", 'blank': 'True'}),
            'target_person_attendance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_PERSON_ATTENDANCE'", 'blank': 'True'}),
            'videoes_screened': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Video']", 'symmetrical': 'False'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.state': {
            'Meta': {'object_name': 'State', 'db_table': "u'STATE'"},
            'country': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Country']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'STATE_NAME'"})
        },
        'dashboard.target': {
            'Meta': {'unique_together': "(('district', 'month_year'),)", 'object_name': 'Target'},
            'adoption_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_attendance_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'challenges': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'clusters_identification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crp_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crp_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_identification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dg_concept_sharing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dissemination_set_deployment': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disseminations': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'editor_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'editor_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exp_interest_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'month_year': ('django.db.models.fields.DateField', [], {}),
            'storyboard_preparation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'support_requested': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video_editing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_production': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_quality_checking': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_shooting': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_uploading': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'village_operationalization': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'villages_certification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'what_not_went_well': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'what_went_well': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'dashboard.training': {
            'Meta': {'unique_together': "(('training_start_date', 'training_end_date', 'village'),)", 'object_name': 'Training', 'db_table': "u'TRAINING'"},
            'animators_trained': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Animator']", 'symmetrical': 'False'}),
            'development_manager_present': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.DevelopmentManager']", 'null': 'True', 'db_column': "'dm_id'", 'blank': 'True'}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'db_column': "'fieldofficer_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'training_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_END_DATE'"}),
            'training_outcome': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_OUTCOME'", 'blank': 'True'}),
            'training_purpose': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_PURPOSE'", 'blank': 'True'}),
            'training_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_START_DATE'"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.traininganimatorstrained': {
            'Meta': {'object_name': 'TrainingAnimatorsTrained', 'db_table': "u'TRAINING_animators_trained'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']", 'db_column': "'animator_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'training': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Training']", 'db_column': "'training_id'"})
        },
        'dashboard.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'district_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.video': {
            'Meta': {'unique_together': "(('title', 'video_production_start_date', 'video_production_end_date', 'village'),)", 'object_name': 'Video', 'db_table': "u'VIDEO'"},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'ACTORS'"}),
            'approval_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'APPROVAL_DATE'", 'blank': 'True'}),
            'audio_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'AUDIO_QUALITY'", 'blank': 'True'}),
            'cameraoperator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'cameraoperator'", 'to': "orm['dashboard.Animator']"}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'DURATION'", 'blank': 'True'}),
            'edit_finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_FINISH_DATE'", 'blank': 'True'}),
            'edit_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_START_DATE'", 'blank': 'True'}),
            'editing_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'EDITING_QUALITY'", 'blank': 'True'}),
            'facilitator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'facilitator'", 'to': "orm['dashboard.Animator']"}),
            'farmers_shown': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Person']", 'symmetrical': 'False'}),
            'final_edited_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'FINAL_EDITED_FILENAME'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Language']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'movie_maker_project_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'MOVIE_MAKER_PROJECT_FILENAME'", 'blank': 'True'}),
            'picture_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'PICTURE_QUALITY'", 'blank': 'True'}),
            'raw_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'RAW_FILENAME'", 'blank': 'True'}),
            'related_practice': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Practices']", 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'db_column': "'REMARKS'", 'blank': 'True'}),
            'reviewer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Reviewer']", 'null': 'True', 'blank': 'True'}),
            'storybase': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'STORYBASE'"}),
            'storyboard_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'STORYBOARD_FILENAME'", 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'supplementary_video_produced': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'null': 'True', 'blank': 'True'}),
            'thematic_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'THEMATIC_QUALITY'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'TITLE'"}),
            'video_production_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_END_DATE'"}),
            'video_production_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_START_DATE'"}),
            'video_suitable_for': ('django.db.models.fields.IntegerField', [], {'db_column': "'VIDEO_SUITABLE_FOR'"}),
            'video_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'VIDEO_TYPE'"}),
            'viewers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"}),
            'youtubeid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'YOUTUBEID'", 'blank': 'True'})
        },
        'dashboard.videosscreenedinscreening': {
            'Meta': {'object_name': 'VideosScreenedInScreening', 'db_table': "u'SCREENING_videoes_screened'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village', 'db_table': "u'VILLAGE'"},
            'block': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Block']"}),
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CONTROL'", 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'no_of_households': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'NO_OF_HOUSEHOLDS'", 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'POPULATION'", 'blank': 'True'}),
            'road_connectivity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'ROAD_CONNECTIVITY'", 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        },
        'dashboard.villageprecalculation': {
            'Meta': {'unique_together': "(('village', 'date'),)", 'object_name': 'VillagePrecalculation', 'db_table': "u'village_precalculation'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_active_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adopted_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adoption_by_active': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'website.activity': {
            'Meta': {'object_name': 'Activity'},
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Collection']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Farmer']", 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.ImageSpec']", 'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Partner']", 'null': 'True', 'blank': 'True'}),
            'textContent': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.User']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        },
        'website.badge': {
            'Meta': {'object_name': 'Badge'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        },
        'website.collection': {
            'Meta': {'object_name': 'Collection'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_collections'", 'to': "orm['website.Country']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'language_collections'", 'max_length': '20', 'to': "orm['website.Language']"}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_collections'", 'to': "orm['website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'video_collections'", 'symmetrical': 'False', 'to': "orm['website.Video']"})
        },
        'website.comment': {
            'Meta': {'object_name': 'Comment'},
            'activityURI': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_activity'", 'null': 'True', 'to': "orm['website.Activity']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'farmer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'farmer_comments'", 'null': 'True', 'to': "orm['website.Farmer']"}),
            'inReplyToCommentUID': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['website.Comment']"}),
            'isOnline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_comments'", 'null': 'True', 'to': "orm['website.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_comments'", 'null': 'True', 'to': "orm['website.Video']"})
        },
        'website.country': {
            'Meta': {'object_name': 'Country'},
            'countryName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'website.farmer': {
            'Meta': {'object_name': 'Farmer'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['website.Collection']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'farmer_interests'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['website.Interests']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Partner']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.filtervaluedescription': {
            'Meta': {'object_name': 'FilterValueDescription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemCount': ('django.db.models.fields.BigIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'website.imagespec': {
            'Meta': {'object_name': 'ImageSpec'},
            'altString': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageLinkURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'website.interests': {
            'Meta': {'object_name': 'Interests'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        'website.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.partner': {
            'Meta': {'object_name': 'Partner'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collectionCount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'joinDate': ('django.db.models.fields.DateField', [], {}),
            'likes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'logoURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'videos': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'website.searchcompletion': {
            'Meta': {'object_name': 'SearchCompletion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'searchTerm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'targetURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'website.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'website.user': {
            'Meta': {'object_name': 'User'},
            'authToken': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'avatarURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'facebookID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'linkedInID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitterID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'adoptions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'language_videos'", 'max_length': '20', 'to': "orm['website.Language']"}),
            'offlineLikes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offlineViews': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineLikes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'onlineViews': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partner_videos'", 'to': "orm['website.Partner']"}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subsector': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'subtopic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['website.Tag']", 'symmetrical': 'False'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'youtubeID': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.videowatchrecord': {
            'Meta': {'object_name': 'VideoWatchRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeWatched': ('django.db.models.fields.BigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_watchrecord'", 'to': "orm['website.User']"}),
            'videoUID': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_watchrecord'", 'to': "orm['website.Video']"})
        }
    }

    complete_apps = ['dashboard', 'website']
    symmetrical = True
