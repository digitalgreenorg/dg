import datetime
import dashboard.models
from django.core.exceptions import ObjectDoesNotExist
import os
import pickle
import sqlite3
import sys
import urllib2
from urllib import urlencode
from sync_classes import *
from create_querystring import *
   
# Usage
# sync_scripts.fix_sync_issue.sync("person_adopt_practice","C:\\Users\\hp\\Desktop\\digital Green\\dg\\task1_statistics\\baif_hunsur_2012-06-21_18-39_adoption_data","C:\\Users\\hp\\Desktop\\digital Green\\digitalgreendatabase_hunsur.sqlite","http://127.0.0.1:8000")

def unpickleData(use_pickle_file) :
    data = pickle.load(open(use_pickle_file,"rb"))
    return data

def write_data(save_data,file_suffix,user):
    dir_name =os.path.dirname(os.path.realpath(sys.argv[0]))+"\\sync_scripts\\fix_data_statistics\\"
    if not (os.path.isdir(dir_name)):
        os.makedirs(dir_name)
    now = datetime.datetime.now()
    file =  dir_name+user+"_"+now.strftime("%Y-%m-%d_%H-%M")+"_"+file_suffix
    pickle.dump(save_data,open(file,"wb"))

def fetch_missing_from_online_ids(use_pickle_file):
    data = unpickleData(use_pickle_file)
    missing_from_online_ids=[]
    if(len(data['ids_missing_from_online_and_formq'])!=0):
        missing_from_online_ids = data['ids_missing_from_online_and_formq']

    if(len(data['ids_missing_from_online_and_status_1'])!=0):
        missing_from_online_ids.extend(data['ids_missing_from_online_and_status_1'])

    if(len(data['ids_missing_from_online_and_status_0'])!=0):
        missing_from_online_ids.extend(data['ids_missing_from_online_and_status_0'])
    
    return missing_from_online_ids

    
    
def fix_attendance_issue_for_screening(s_id,use_local_db,domain):
    local_db = AccessLocalDb(use_local_db,screening_table)
    if(domain[len(domain)-1]=="/"):
        domain=domain[:len(domain)-1]
    sync_successfull_attendance_ids=[]
    sync_unsuccessfull_attendance_ids=[]
    attendance = local_db.get_screening_attendance(s_id)
    for item in attendance:
        formq_string = person_meeting_attendance_table['create_formq_string'](item)
        url = domain+person_meeting_attendance_table['add_url']
        print formq_string
        print url
        req = urllib2.Request(url, formq_string)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            print "url incorrect"
            sys.exit()
        except Exception:
            save_data = {'sync_successfull_ids':[],'sync_unsuccessfull_ids':[],'sync_successfull_attendance_ids':sync_successfull_attendance_ids,'sync_unsuccessfull_attendance_ids':sync_unsuccessfull_attendance_ids}
            write_data(save_data,"attendance",local_db.get_user())
            raise Exception
        r=response.read()
        print r
        if(r=="1"):
            sync_successfull_attendance_ids.append((s_id,item[0]))
        else:
            sync_unsuccessfull_attendance_ids.append((s_id,item[0]))
                
    save_data = {'sync_successfull_ids':[],'sync_unsuccessfull_ids':[],'sync_successfull_attendance_ids':sync_successfull_attendance_ids,'sync_unsuccessfull_attendance_ids':sync_unsuccessfull_attendance_ids}
    write_data(save_data,"attendance",local_db.get_user())
    
def sync(table_name,use_pickle_file,use_local_db,domain):
    found=0
    for table in check_tables:
        if(table['table_name_in_local_db']==table_name):
            check_table = table
            found=1
            break    
    if(found==0):
        print "No such table exists in local database"        
        sys.exit()
    if(domain[len(domain)-1]=="/"):
        domain=domain[:len(domain)-1]
    local_db = AccessLocalDb(use_local_db,check_table)            
    missing_from_online_ids = fetch_missing_from_online_ids(use_pickle_file)
    sync_successfull_ids=[]
    sync_unsuccessfull_ids =[]
    sync_successfull_attendance_ids=[]
    sync_unsuccessfull_attendance_ids=[]
    count=0
    for s_id in missing_from_online_ids:
        count+=1
        row = local_db.get_table_data_by_id(s_id)
        formq_string=""
        if(check_table['table_id']==29):
            formq_string =check_table['create_formq_string'](row,local_db)
        else:
            formq_string =check_table['create_formq_string'](row)
        url = domain+check_table['add_url']
        req = urllib2.Request(url, formq_string)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            print "url incorrect"
            sys.exit()
        except Exception:
            save_data = {'sync_successfull_ids':sync_successfull_ids,'sync_unsuccessfull_ids':sync_unsuccessfull_ids,'sync_successfull_attendance_ids':sync_successfull_attendance_ids,'sync_unsuccessfull_attendance_ids':sync_unsuccessfull_attendance_ids}
            write_data(save_data,check_table['pickle_file'],local_db.get_user())
            raise Exception
        r = response.read()
        print str(count)+" "+r
        if(r =="1"):
            sync_successfull_ids.append(s_id)
            if(check_table['table_id']==SCREENING_TABLE_ID):
                print "syncing attendance"
                attendance = local_db.get_screening_attendance(s_id)
                for item in attendance:
                    formq_string = person_meeting_attendance_table['create_formq_string'](item)
                    url = domain+person_meeting_attendance_table['add_url']
                    req = urllib2.Request(url, formq_string)
                    try:
                        response = urllib2.urlopen(req)
                    except urllib2.URLError:
                        print "url incorrect"
                        sys.exit()
                    except Exception:
                        save_data = {'sync_successfull_ids':sync_successfull_ids,'sync_unsuccessfull_ids':sync_unsuccessfull_ids,'sync_successfull_attendance_ids':sync_successfull_attendance_ids,'sync_unsuccessfull_attendance_ids':sync_unsuccessfull_attendance_ids}
                        write_data(save_data,check_table['pickle_file'],local_db.get_user())
                        raise Exception
                    r=response.read()
                    print r
                    if(r=="1"):
                        sync_successfull_attendance_ids.append((s_id,item[0]))
                    else:
                        sync_unsuccessfull_attendance_ids.append((s_id,item[0]))
        else :
            sync_unsuccessfull_ids.append(s_id)
    save_data = {'sync_successfull_ids':sync_successfull_ids,'sync_unsuccessfull_ids':sync_unsuccessfull_ids,'sync_successfull_attendance_ids':sync_successfull_attendance_ids,'sync_unsuccessfull_attendance_ids':sync_unsuccessfull_attendance_ids}
    write_data(save_data,check_table['pickle_file'],local_db.get_user());
    print "done"

    