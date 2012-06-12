#Python Script for calculating inconsistencies in database. It can be run as Cron
# Requires Error and Rule models
#
#For adding new Rule
# 1. Add a new entry in the Rule model
# 2. Add a new function for the rule
# General structure of def rule() ---
#     def rule():
#        rule = Rule.objects.get(pk= ID) ***ID is hard-coded***
#        sql = sql for calculation the errors
#        run sql on database
#        new_errors = post processing on returned results from database. Create a list of Error objects
#        old_errors = errors.objects.filter(rule = rule)
#        syncErrors(new_errors, old_errors)
#
# 3. Add a call to the new rule at the bottom of this script
import site, sys
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')

from django.core.management import setup_environ
import settings

setup_environ(settings)
from django.db import connection, IntegrityError
from dashboard.models import *

cursor = connection.cursor()

#Function for syncing errors i.e. Add new errors and remove resolved errors
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

#check equality of errors
def compareErrors(error1, error2):
    return isinstance(error2, error1.__class__) \
                and error1.rule.id == error2.rule.id \
                and error1.content_type1.id == error2.content_type1.id \
                and error1.object_id1 == error2.object_id1 \
                and ((error1.content_type2 == None and error2.content_type2 == None) or error1.content_type2.id == error2.content_type2.id) \
                and error1.object_id2 == error2.object_id2

#rule Id:1; Name = Screening with same date and same PG
def rule1():
    rule = Rule.objects.all()[0]
    sql = """SELECT sc.id as object_id, B.district_id, sfgt.persongroups_id, sc.date
        FROM SCREENING_farmer_groups_targeted sfgt
        JOIN SCREENING sc ON sc.id = sfgt.screening_id
        JOIN (SELECT date, persongroups_id 
            FROM SCREENING_farmer_groups_targeted sfgt
            JOIN SCREENING sc on sc.id = sfgt.screening_id
            GROUP BY date, persongroups_id
            HAVING COUNT(*) > 1) t ON t.date = sc.date and t.persongroups_id = sfgt.persongroups_id
        JOIN VILLAGE V ON V.id = sc.village_id
        JOIN BLOCK B ON B.id = V.block_id
        ORDER BY sfgt.persongroups_id, sc.date, sc.id"""
    
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
    
    
#rule Id:2; Name = Screening date after today    
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

#rule Id:3; Name = Screening with videos from other state
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
            
#rule Id:4; Name = Video Production took long time
def rule4():
    rule = Rule.objects.get(pk=4)
    sql = """SELECT VID.id as content_object1, B.district_id
    FROM VIDEO VID
    JOIN VILLAGE V ON V.id = VID.village_id
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
    
#rule Id:5; Name = Video not shown in any screening
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
    
#rule Id:6; Name = Video production end date is before video production start date.
def rule6():
    rule = Rule.objects.get(pk=6)
    sql = """SELECT VID.id as content_object1, B.district_id
    FROM VIDEO VID
    JOIN VILLAGE V ON V.id = VID.village_id
    JOIN BLOCK B ON B.id = V.block_id
    WHERE VIDEO_PRODUCTION_END_DATE < VIDEO_PRODUCTION_START_DATE
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

#rule Id:7; Name = Video production end date is after today    
def rule7():
    rule = Rule.objects.get(pk=7)
    sql = """SELECT VID.id as content_object1, B.district_id
    FROM VIDEO VID
    JOIN VILLAGE V ON V.id = VID.village_id
    JOIN BLOCK B ON B.id = V.block_id
    WHERE VIDEO_PRODUCTION_END_DATE > CURDATE()
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

#rule Id:8; Name = Video productoin end date is after the date of screening of that video
def rule8():
    rule = Rule.objects.get(pk=8)
    sql = """SELECT SC.id as content_object1, VID.id as content_object2, B.district_id
    FROM SCREENING_videoes_screened SVS
    JOIN SCREENING SC on SC.id = SVS.screening_id
    JOIN VIDEO VID on VID.id = SVS.video_id
    JOIN VILLAGE V ON V.id = SC.village_id
    JOIN BLOCK B ON B.id = V.block_id
    WHERE VIDEO_PRODUCTION_END_DATE > DATE
    """

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
    
#rule Id:9; Name = Screening end time is less than or same as start time   
def rule9():
    rule = Rule.objects.get(pk=9)
    sql = """SELECT SC.id as object_id, B.district_id 
    FROM SCREENING SC
    JOIN VILLAGE V ON V.id = SC.village_id
    JOIN BLOCK B ON B.id = V.block_id   
    WHERE END_TIME <= START_TIME
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

rule1()
rule2()
rule3()
rule4()
rule5()
rule6()
rule7()
rule8()
rule9()

cursor.close()
connection.close()
