from django.core.management import setup_environ
import settings
setup_environ(settings)
from dashboard.models import *
            
def  merge_pmas(scr1,scr2):
    pma_list=PersonMeetingAttendance.objects.filter(screening=scr1).values_list('person_id')
    pmas=PersonMeetingAttendance.objects.filter(screening=scr2)
    for j in pmas:
        if (j.person_id,) not in pma_list:
            j.screening_id=scr1.id
            j.save()

def delete_scr(scr2):
    scr2.delete()
    
def merge_groups(scr1,scr2):
    group_list= GroupsTargetedInScreening.objects.filter(screening=scr1).values_list('persongroups')
    pgs= GroupsTargetedInScreening.objects.filter(screening=scr2)
    for j in pgs:
        if (j.persongroups_id,) not in group_list:
            j.screening_id=scr1.id
            j.save()
                        
def merge_videos(scr1,scr2):
    vid_list= VideosScreenedInScreening.objects.filter(screening=scr1).values_list('video')
    vids= VideosScreenedInScreening.objects.filter(screening=scr2)
    for j in vids:
        if (j.video_id,) not in vid_list:
            j.screening_id=scr1.id
            j.save()
                 
def merge_screenings(scr1,scr2):
    if (set(scr1.videoes_screened.all())!=set(scr2.videoes_screened.all())):
        merge_videos(scr1, scr2)
    if (set(scr1.farmer_groups_targeted.all())!=set(scr2.farmer_groups_targeted.all())):
        merge_groups(scr1, scr2)
    merge_pmas(scr1, scr2)
    delete_scr(scr2)
    
#def animator_unique_together_migration():
#    dup_list=Animator.objects.values('name','gender','partner').annotate(sameanimator=Count('name')).filter(sameanimator__gt=1)
#    for i in dup_list:
#        make_unique=Animator.objects.filter(name=i['name'],gender=i['gender'],partner=i['partner'])
#        for j in range(len(make_unique)):
#            print 'modifying animator with name, id, partner,village', make_unique[j].name, make_unique[j].id, make_unique[j].partner.partner_name, make_unique[j].village.village_name
#            final_animator_name = make_unique[j].name + ' ('+make_unique[j].village.village_name +')'
#            make_unique[j].name = final_animator_name
#            make_unique[j].save()
#            print 'after modifying animator: name, id, partner,village', make_unique[j].name, make_unique[j].id, make_unique[j].partner.partner_name, make_unique[j].village.village_name
#    dup_list=Animator.objects.values('name','gender','partner').annotate(sameanimator=Count('name')).filter(sameanimator__gt=1)
#    print 'migration complete..Dups remaining:',len(dup_list)

def clean_person_group_screening():
    grp_dupes=PersonGroups.objects.values('village','group_name').annotate(sameper=Count('village')).filter(sameper__gt=1)
    for i in grp_dupes:
        make_unique=PersonGroups.objects.filter(group_name=i['group_name'],village=i['village'])
        for j in range(len(make_unique)):
            temp= make_unique[j].group_name + unicode(j)
            make_unique[j].group_name=temp
            make_unique[j].save()
    
    dup_list=Person.objects.values('person_name','father_name','village').annotate(sameper=Count('person_name')).filter(sameper__gt=1)
    for i in dup_list:
        make_unique=Person.objects.filter(person_name=i['person_name'],father_name=i['father_name'],village=i['village'])
        for j in range(len(make_unique)):
            if len(set(make_unique.values_list('group')))==1:
                temp= make_unique[j].person_name + unicode(j)
                make_unique[j].person_name=temp
                make_unique[j].save()
            elif make_unique[j].group == None:
                temp= make_unique[j].person_name + unicode(j)
                make_unique[j].person_name=temp
                make_unique[j].save()
            else:
                temp= make_unique[j].father_name+u'-('+make_unique[j].group.group_name+u')'
                make_unique[j].father_name=temp
                make_unique[j].save()
    dup_list=Person.objects.values('person_name','father_name','village').annotate(sameper=Count('person_name')).filter(sameper__gt=1)
    print len(dup_list)          
    scr_dupes=Screening.objects.values('village','date','start_time','end_time','animator').annotate(samescr=Count('village')).filter(samescr__gt=1)
    for i in scr_dupes:
        to_del=Screening.objects.filter(village=i['village'],date=i['date'],start_time=i['start_time'],end_time=i['end_time'],animator=i['animator'])
        if(i['samescr'])==2:
            merge_screenings(to_del[0],to_del[1])
        else:
            for j in to_del[1:]:
                merge_screenings(to_del[0],j)
    if len(Screening.objects.values('village','date','start_time','end_time','animator').annotate(samescr=Count('village')).filter(samescr__gt=1))==0:
        print "Screening data cleaned successfully"
            
            