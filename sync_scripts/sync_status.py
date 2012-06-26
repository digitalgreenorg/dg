import datetime
import os
import pickle
import sys
from sync_classes import *

def get_sync_status(use_local_db):			
    dir_name =os.path.dirname(os.path.realpath(sys.argv[0]))+"\\sync_scripts\\sync_status_statistics\\"
    if not (os.path.isdir(dir_name)):
        os.makedirs(dir_name)
    for check_table in check_tables:
        print "checking "+check_table['table_name_in_local_db']+" ...."
        exists_in_both =0
        ids_exists_in_both=[]
        missing_from_online_and_formq=0
        ids_missing_from_online_and_formq=[]  
        missing_from_online_and_status_1=0
        ids_missing_from_online_and_status_1=[]
        missing_from_online_and_status_0=0
        ids_missing_from_online_and_status_0=[]
        local_db = AccessLocalDb(use_local_db,check_table)
        online_db = AccessOnlineDb()
        count=0
        screening=local_db.get_next_id()
        while(screening!=None):
            count+=1
            if(online_db.id_exists(screening[0],check_table['table_name_in_online_db'])):
                exists_in_both+=1
                ids_exists_in_both.append(screening[0])
            else:
                if not(local_db.id_exists_in_formQ(screening[0])):
                    missing_from_online_and_formq+=1
                    ids_missing_from_online_and_formq.append(screening[0])
                else:
                    if(local_db.id_sync_status(screening[0])==0):
                        missing_from_online_and_status_0+=1
                        ids_missing_from_online_and_status_0.append(screening[0])
                    else:
                        missing_from_online_and_status_1+=1
                        ids_missing_from_online_and_status_1.append(screening[0])
            screening=local_db.get_next_id()	        
        save_data ={'exists_in_both':exists_in_both, 'ids_exists_in_both':ids_exists_in_both,\
        'missing_from_online_and_formq':missing_from_online_and_formq,'ids_missing_from_online_and_formq':ids_missing_from_online_and_formq,\
        'missing_from_online_and_status_0':missing_from_online_and_status_0,'ids_missing_from_online_and_status_0':ids_missing_from_online_and_status_0,\
        'missing_from_online_and_status_1':missing_from_online_and_status_1,'ids_missing_from_online_and_status_1':ids_missing_from_online_and_status_1}
        print "exists in both online and offline: "+str(exists_in_both)
        print "missing from online and formq: "+str(missing_from_online_and_formq)	
        print "missing from online and formq status 0: "+str(missing_from_online_and_status_0)
        print "missing from online and formq status 1: "+str(missing_from_online_and_status_1)
        now = datetime.datetime.now()
        file =  dir_name+local_db.get_user()+"_"+now.strftime("%Y-%m-%d_%H-%M")+"_"+check_table['pickle_file']
        pickle.dump(save_data,open(file,"wb"))
