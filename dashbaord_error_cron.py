
from django.core.management import setup_environ
import settings

setup_environ(settings)
from django.db import connection, IntegrityError
from dashboard.models import *

cursor = connection.cursor()

#Function from syncing errors i.e. Add new errors and remove resolved errors
#new_errors: list of actual errors
#old_errors: list of errors in Errors table
#Algo: Delete all the common errors from both the list. Then,
#         (New - Common) = To be added.
#         (Old - common) = to be deleted
def syncErrors(new_errors, old_errors):
    #deleting all the intersection set from both, old_errors & new_errors    
    i = 0
    while i< len(old_errors):
        j = 0
        flag = 0
        while j < len(new_errors):
            if(compareErrors(old_errors[i], new_errors[j])):
                new_errors.pop(j)
                flag = 1
            else:
                j = j+1
        if(flag):
            old_errors.pop(i)
        else:
            i = i + 1
    
    #Cleaning new_errors. Deleting identical errors within new_errors to prevent integrity errors
    i =0
    while i< len(new_errors):
        j = i+1
        while j < len(new_errors):
            while(compareErrors(new_errors[i], new_errors[j])):
                new_errors.pop(j)
            j = j+1
        i = i+1
    
    for error in new_errors:
        error.save();
    for error in old_errors:
        error.delete();
            
def compareErrors(error1, error2):
    return isinstance(error2, error1.__class__) \
                and error1.rule == error2.rule \
                and error1.content_type1 == error2.content_type1 \
                and error1.content_type2 == error2.content_type2 \
                and error1.object_id1 == error2.object_id1 \
                and error1.object_id2 == error2.object_id2
                
def rule1():
    rule = Rule.objects.all()[0]
    sql = """SELECT sc.id as object_id, b.district_id, sfgt.persongroups_id, sc.date
        FROM screening_farmer_groups_targeted sfgt
        JOIN screening sc on sc.id = sfgt.screening_id
        JOIN (SELECT date, persongroups_id FROM screening_farmer_groups_targeted sfgt
        join screening sc on sc.id = sfgt.screening_id
        group by date, persongroups_id
        having count(*) > 1) t on t.date = sc.date and t.persongroups_id = sfgt.persongroups_id
        JOIN VILLAGE V ON V.id = sc.village_id
        JOIN BLOCK B ON B.id = V.block_id
        order by sfgt.persongroups_id, sc.date, sc.id"""
    
    new_errors = [];
    if cursor.execute(sql):
        rows = cursor.fetchall()
        cur = rows[0]
        for row in rows[1:]:
            if row[2] == cur[2] and row[3] == cur[3]:
                new_errors.append(Error(content_object1 = Screening.objects.get(pk=cur[0]), \
                             content_object2 = Screening.objects.get(pk=row[0]), \
                             district = District.objects.get(pk=row[1]), \
                             rule = rule))
            else:
                cur = row;
    
    old_errors = list(Error.objects.filter(rule = rule))
    syncErrors(new_errors, old_errors)
    
def rule2():
    rule = Rule.objects.get(pk=2)
    sql = """SELECT SC.id as object_id, B.district_id 
    FROM SCREENING SC
    JOIN VILLAGE V ON V.id = SC.village_id
    JOIN BLOCK B ON B.id = V.block_id   
    WHERE DATE > CURDATE()
    """
    
    new_errors = []
    if cursor.execute(sql):
        rows = cursor.fetchall()
        for row in rows:
            dist = District.objects.get(pk=row[1])
            new_errors.append(Error(content_object1=Screening.objects.get(pk=row[0]), \
                                 district = dist,
                                 rule = rule))

    old_errors = list(Error.objects.filter(rule = rule))
    syncErrors(new_errors, old_errors)

def rule3():
    rule = Rule.objects.get(pk=3)
    sql = """SELECT SC.id as content_object1, VID.id as content_object2, B.district_id
    FROM SCREENING_videoes_screened SVS
    JOIN SCREENING SC on SC.id = SVS.screening_id
    JOIN VIDEO VID on VID.id = SVS.video_id
    JOIN VILLAGE V ON V.id = SC.village_id
    JOIN BLOCK B ON B.id = V.block_id
    JOIN DISTRICT D ON D.id = B.district_id
    JOIN VILLAGE V1 ON V1.id = VID.village_id
    JOIN BLOCK B1 ON B1.id = V1.block_id
    JOIN DISTRICT D1 ON D1.id = B1.district_id
    WHERE D.state_id != D1.state_id"""
    
    new_errors = []
    if cursor.execute(sql):
        rows = cursor.fetchall()
        for row in rows:
            new_errors.append(Error(content_object1=Screening.objects.get(pk=row[0]), \
                                 content_object2 = Video.objects.get(pk=row[1]),
                                 district = District.objects.get(pk=row[2]),
                                 rule = rule))
    old_errors = list(Error.objects.filter(rule = rule))
    syncErrors(new_errors, old_errors)
            
def rule4():
    rule = Rule.objects.get(pk=4)
    sql = """SELECT VID.id as content_object1, B.district_id
    FROM VIDEO VID
    JOIN VILLAGE V ON V.id = vid.village_id
    JOIN BLOCK B ON B.id = V.block_id
    WHERE DATEDIFF(VIDEO_PRODUCTION_END_DATE , VIDEO_PRODUCTION_START_DATE) > 12"""
    
    new_errors = []
    if cursor.execute(sql):
        rows = cursor.fetchall()
        for row in rows:
            dist = District.objects.get(pk=row[1])
            new_errors.append(Error(content_object1=Video.objects.get(pk=row[0]), \
                                 district = dist,
                                 rule = rule))
    
    old_errors = list(Error.objects.filter(rule = rule))
    syncErrors(new_errors, old_errors)

def rule5():
    rule = Rule.objects.get(pk=5)
    sql = """SELECT VID.id as content_object1, B.district_id
    FROM VIDEO VID
    JOIN VILLAGE V ON V.id = VID.village_id
    JOIN BLOCK B ON B.id = V.block_id
    WHERE VID.id NOT IN (SELECT video_id FROM SCREENING_videoes_screened SVS)
    and VIDEO_SUITABLE_FOR != 4
    """

    new_errors = []   
    if cursor.execute(sql):
        rows = cursor.fetchall()
        for row in rows:
            dist = District.objects.get(pk=row[1])
            new_errors.append(Error(content_object1=Video.objects.get(pk=row[0]), \
                                 district = District.objects.get(pk=row[1]),
                                 rule = rule))
    
    old_errors = list(Error.objects.filter(rule = rule))
    syncErrors(new_errors, old_errors)

rule1()
rule2()
rule3()
rule4()
rule5()