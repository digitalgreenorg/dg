import glob, os
from django.core.management import setup_environ
import settings
setup_environ(settings)
from dashboard.models import *
from django.db.models import Count
from datetime import datetime, timedelta
import datetime
import time
import csv
from farmerbook import get_id_with_images

def grade1(village_info):
    target_disseminations = 2
    grade = []
    for vill_id in village_id:
        per_month_ratio = 0
        for i in range(0,6):
            ratio = 0
            date1 = grading_start_date + timedelta(hours = i*720)
            date2 = date1 + timedelta(hours=720)
            screenings_per_group = []
            screenings_per_group = Screening.objects.filter(village = vill_id, date__range = [date1,date2]).values('farmer_groups_targeted').annotate(num_scr = Count('id'))
            if(screenings_per_group):
                for record in screenings_per_group:
                    if(record['num_scr']>2):
                        record['num_scr'] = 2
                    ratio += float(record['num_scr'])/target_disseminations
                ratio = ratio/len(screenings_per_group)
            per_month_ratio +=ratio
        per_month_ratio = per_month_ratio/6.0   # for 6 months
        vil_name = Village.objects.filter(id = vill_id).values_list('village_name', flat=True)[0]
        grade.append({'id': vill_id, 'vil_name': vil_name,
        'grade_ratio': per_month_ratio})
    print "Grade 1 done "
    return grade
       
    
def grade2(village_info):
    grade = []
    for vill_id in village_id:
        ratio = 0
        screenings = Screening.objects.filter(village = vill_id, date__range = [grading_start_date, grading_end_date]).values_list('id', flat=True)
        person_ids = Person.objects.filter(village__id = vill_id, group__isnull = False).values_list('id', flat=True)
        for scr in screenings:
            persons_attended = PersonMeetingAttendance.objects.filter(screening__id = scr).exclude(person__group__isnull=True).count()
            persons_targeted_qs = Screening.objects.filter(id=scr).values('id').annotate(
                            num_total = Count('farmer_groups_targeted__person__id', distinct=True))
            persons_targeted = persons_targeted_qs[0]['num_total']
            if persons_attended > persons_targeted:
                ratio += 1.0
            else:
                if persons_targeted:
                    ratio += float(persons_attended) / persons_targeted
                else:
                    ratio += 0
        if len(screenings):
            ratio = ratio / len(screenings)
        else:
            ratio = 0
        grade.append({'id': vill_id,
                      'grade_ratio': ratio})
    print "Grade 2 done "
    return grade  

def grade3(village_info):
    grade = []
    for vill_id in village_info:
        farmer = PersonMeetingAttendance.objects.filter(person__village = vill_id, screening__date__range = [grading_start_date, grading_end_date]).values('person').annotate(screenings_attended = Count('screening'))
        groups = PersonGroups.objects.filter(village = vill_id).values_list('id', flat = True)
        ratio = 0
        if groups:
            for group in groups:
                total = Person.objects.filter(group = group).count()
                active = farmer.filter(person__group = group).count()
                if total:
                    ratio += float(active)/total
                    
                ratio = ratio / len(groups)    
        grade.append({'id': vill_id,
                      'grade_ratio': ratio})
    print "Grade 3 done "
    return grade   

# takes around 7-8 mins to run. 
def grade4(village_info):
    grade = []
    for vill_id in village_info:
        ratio = 0
        adopted_list = []
        screenings_list = Screening.objects.filter(village = vill_id, date__range = [grading_start_date, grading_end_date]).values_list('id', 'videoes_screened')
        if(screenings_list):
            for scr,vid in screenings_list:
                persons = PersonMeetingAttendance.objects.filter(screening = scr).values_list('person', flat = True)
                total = len(persons)/10.0        # for 10 %
                if(total):
                    adopted = PersonAdoptPractice.objects.filter(video = vid, person__in = persons).exclude(id__in = adopted_list).values_list('id',flat=True)
                    for adopt_id in adopted:
                        adopted_list.append(adopt_id)
                    adopted_count = len(adopted)
                    temp_ratio = float(adopted_count)/total
                    if(temp_ratio > 1):
                        temp_ratio = 1.0
                    ratio += temp_ratio
            ratio = ratio/len(screenings_list)
        else:
            ratio = 0   
        grade.append({'id': vill_id,
                      'grade_ratio': ratio})
    print "Grade 4 done "
    return grade
            
def grade5_6(village_info):
    grade = []
    #Quality of dissemination gauged through number of questions/ comments  
    for i in village_info:
        questions_ratio = 0
        interest_ratio = 0 
        vil_id = i
        screenings_conducted_in_vil = Screening.objects.filter(date__range = (grading_start_date, grading_end_date), village__id = vil_id).values_list('id', flat=True)
        sum_per_ques = 0
        sum_per_interest = 0
        for sc in screenings_conducted_in_vil:
            ques = PersonMeetingAttendance.objects.filter(screening__id = sc).exclude(expressed_question='').count()
            interests = PersonMeetingAttendance.objects.filter(screening__id = sc, interested=1).count()
            atten = PersonMeetingAttendance.objects.filter(screening__id = sc).count()
            if interests:
                ratio_per_interest = interests / (0.3 * atten)
                if ratio_per_interest > 1:
                    ratio_per_interest = 1
            else:
                ratio_per_interest = 0
            #calculate 15% of atten and compare it with questions asked
            if ques:
                ratio_per_ques = ques / (0.05 * atten)
                if ratio_per_ques > 1:
                    ratio_per_ques = 1
                #print sum_per_ques, vil_id
            else:
                ratio_per_ques = 0
            sum_per_ques += ratio_per_ques
            sum_per_interest += ratio_per_interest
        #print sum_per_ques
        if len(screenings_conducted_in_vil):
            questions_ratio = sum_per_ques/len(screenings_conducted_in_vil)
            interest_ratio = float(sum_per_interest)/len(screenings_conducted_in_vil)
        grade.append({'id': vil_id,
                      'question_grade_ratio': questions_ratio,
                      'interests_grade_ratio': interest_ratio})
    print 'grade 5 and 6 done'
    return grade
            
            
if __name__ == "__main__":
    print "Working..."
    # village id list containing village which have photos
    grd_file = open('grd_file_5_6.csv', 'wb')
    wrtr = csv.writer(grd_file, delimiter=',', quotechar='"')
    grading_start_date = datetime.date(2012, 1, 1)
    grading_end_date = datetime.date(2012,6, 30)
#    village_id = [10000000000048L, 10000000000052L, 10000000000053L]#, 10000000000067L, 10000000000074L, 10000000000077L, 10000000000078L, 10000000000092L, 10000000000093L, 10000000000112L, 10000000000217L, 10000000000230L, 10000000000242L, 10000000000251L, 10000000000252L, 10000000000254L, 10000000000255L, 10000000000257L, 10000000000260L, 10000000000261L, 10000000000264L, 10000000000265L, 10000000000270L, 10000000000271L, 10000000000272L, 10000000000274L, 10000000000275L, 10000000000276L, 10000000000277L, 10000000000279L, 10000000000280L, 10000000000281L, 10000000000283L, 10000000000284L, 10000000000285L, 10000000000286L, 10000000000287L, 10000000000299L, 10000000000304L, 10000000000305L, 10000000000306L, 10000000000307L, 10000000000309L, 10000000000313L, 10000000000341L, 10000000000342L, 10000000000389L, 10000000000407L, 10000000000408L, 10000000000410L, 10000000000412L, 10000000000414L, 10000000000425L, 10000000000507L, 10000000000514L, 10000000000532L, 10000000000536L, 10000000000537L, 10000000000538L, 10000000018674L, 10000000018676L, 10000000019834L, 10000000019835L, 10000000019841L, 10000000019842L, 10000000019843L, 10000000019854L, 10000000019860L, 10000000019862L, 10000000019864L, 10000000019865L, 10000000019873L, 10000000019874L, 10000000019880L, 10000000019882L, 10000000019883L, 10000000019889L, 10000000019891L, 10000000019901L, 10000000019902L, 10000000019913L, 10000000019918L, 10000000019922L, 10000000019929L, 10000000019942L, 10000000019945L, 10000000019946L, 10000000019954L, 10000000019967L, 10000000019968L, 10000000019969L, 10000000019975L, 10000000019978L, 10000000019985L, 10000000019988L, 10000000020020L, 10000000020029L, 10000000020036L, 10000000020040L, 10000000020047L, 10000000020078L, 10000000020079L, 10000000020082L, 10000000020084L, 10000000020085L, 10000000020090L, 10000000020092L, 10000000020093L, 10000000020104L, 10000000020105L, 10000000020106L, 10000000020110L, 10000000020119L, 10000000020120L, 10000000020154L, 10000000020156L, 10000000020158L, 10000000020183L, 10000000020184L, 10000000020198L, 10000000020199L, 10000000020222L, 10000000020271L, 10000000020345L, 10000000020353L, 10000000020369L, 10000000020370L, 10000000020381L, 10000000020390L, 10000000020391L, 10000000020394L, 10000000020411L, 10000000020412L, 10000000020439L, 10000000020444L, 10000000020448L, 10000000020490L, 10000000020509L, 10000000020517L, 10000000020519L, 10000000020538L, 10000000020555L, 10000000020556L, 10000000020557L, 10000000020562L, 10000000020563L, 10000000020571L, 10000000020572L, 10000000020594L, 10000000020617L, 10000000020625L, 10000000020647L, 10000000020649L, 26000001003L, 26000001007L, 26000001009L, 26000011729L, 47000001038L, 47000001044L, 47000001122L, 47000051353L, 47000052364L, 47000056970L, 47000062452L, 7000001207L]
    village_id = get_id_with_images.get_village_list()
    grade1 = grade1(village_id)
    grade2 = grade2(village_id)
    grade3 = grade3(village_id)
    grade4 = grade4(village_id)
    grade5 = grade5_6(village_id)
    
    
#    wrtr.writerow(['village_id', 'village_name', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Final Grade'])
    grd_file.flush()
    for i in range(len(village_id)):
        final_grade = 20 * grade1[i]['grade_ratio'] + 15 * grade2[i]['grade_ratio'] + 15 * grade3[i]['grade_ratio']
        + 35 * grade4[i]['grade_ratio'] + 5 * grade5[i]['question_grade_ratio'] + 10 * grade5[i]['interests_grade_ratio']
        wrtr.writerow([str(grade1[i]['id']), grade1[i]['vil_name'], grade1[i]['grade_ratio'], grade2[i]['grade_ratio'],  grade3[i]['grade_ratio'],
                       grade4[i]['grade_ratio'],grade5[i]['question_grade_ratio'], grade5[i]['interests_grade_ratio'], final_grade])
        grd_file.flush()
    grd_file.close()
    print 'Done'