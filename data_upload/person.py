import os.path
import dg.settings
import csv

from django.core.management import setup_environ

from geographies.models import Village, Block
from people.models import PersonGroup, Person
from coco.models import CocoUser

setup_environ(dg.settings)

ERROR = 0 #variable to identify if any error occurs in uploaded file
ERROR_FILENAMES = [] #error files to be zipped for download
SUCCESS_FILENAMES = [] #success files to be zipped for download

def upload_data(file, user_id, block_id):
    
    file = os.path.join(dg.settings.MEDIA_ROOT, file)
    
    csvfile = open(file, 'rb')
    rows = csv.DictReader(csvfile)    
    
    req_field = ['Village_Name','Shg_Name','Member_Name','Member_Surname',
                 'Husband_Father_Name','Husband_Father_Surname']
    
    for row in rows:
        if set(req_field) == set(row.keys()) and len(req_field) == len(row.keys()):
            execute_upoad(file, user_id, block_id)
            break
        else:
            return False
    return True            

  
def execute_upoad(file, user_id, block_id):
    global ERROR
    
    user_id = CocoUser.objects.get(user__id=user_id)
    block_id = Block.objects.get(id=block_id)
        
    file_name = str(os.path.splitext(file)[0])
    file_name_list = str(os.path.splitext(file)[0].split('/')[-1])
    
    village_errors_file = open(file_name + '_errors_village.csv', 'wb')
    wrtr = csv.writer(village_errors_file, delimiter=',', quotechar='"')
    wrtr.writerow(["Entry No.", "Village Name", "Error"])
    
    village_success_file = open(file_name + '_success_village.csv', 'wb')
    wrtr_success = csv.writer(village_success_file, delimiter=',',quotechar='"')
    wrtr_success.writerow(["Entry No.", "Village Name"])
    
    csvfile = open(file, 'rb')
    rows_villages = csv.DictReader(csvfile)
        
    village_querry_set = Village.objects.values('village_name','id')
    village_map = dict(village_querry_set)
    
    i = 0 
    for row in rows_villages:
        if str(row['Village_Name']) not in village_map:
            i = i + 1                   
            try:
                village = Village(user_created_id = user_id.id, 
                                  village_name = row['Village_Name'], 
                                  block_id = block_id.id)
                
                village.save()
                village_map[row['Village_Name']] = village.id
                wrtr_success.writerow([i, row['Village_Name']])
                village_success_file.flush()
                print 'pushing', row['Village_Name']
            
            except Exception as e:
                ERROR += 1
                wrtr.writerow([i, row['Village_Name'], e])
                village_errors_file.flush()
    
    village_success_file.close()
    village_errors_file.close()   
    
    ERROR_FILENAMES.append(file_name_list + '_errors_village.csv')
    SUCCESS_FILENAMES.append(file_name_list + '_success_village.csv')
    
    group_errors_file = open(file_name + '_errors_group.csv', 'wb')
    wrtr = csv.writer(group_errors_file, delimiter=',', quotechar='"')
    wrtr.writerow(["Entry No.", "Shg Name", "Error"])
    
    group_success_file = open(file_name + '_success_group.csv', 'wb')
    wrtr_success = csv.writer(group_success_file, delimiter=',', quotechar='"')
    wrtr_success.writerow(["Entry No.", "Shg Name"])

    csvfile = open(file, 'rb')
    rows_groups = csv.DictReader(csvfile)

    group_querry_set = PersonGroup.objects.values('group_name','id')
    group_map = dict(group_querry_set)
    
    i = 0
    for row in rows_groups:
        if str(row['Shg_Name']) + str(row['Village_Name']) not in group_map:
            i = i + 1
            try:                         
                group = PersonGroup(user_created_id = user_id.id,
                                    partner_id = user_id.partner.id,
                                    group_name = row['Shg_Name'], 
                                    village_id = village_map[row['Village_Name']])
                
                group.save()
                group_map[row['Shg_Name'] + row['Village_Name']] = group.id
                wrtr_success.writerow([i,row['Shg_Name']])
                group_success_file.flush()
                print 'pushing', row['Shg_Name']
            
            except Exception as e:
                ERROR += 1
                wrtr.writerow([i, row['Shg_Name'], e] )
            group_errors_file.flush()

    group_errors_file.close()
    group_success_file.close()
    
    ERROR_FILENAMES.append(file_name_list + '_errors_group.csv')
    SUCCESS_FILENAMES.append(file_name_list + '_success_group.csv')
        
    person_errors_file = open(file_name + '_errors_person.csv', 'wb')
    wrtr = csv.writer(person_errors_file, delimiter=',', quotechar='"')
    wrtr.writerow(["Entry No.", "Person Name", "Error"])
    
    person_success_file = open(file_name + '_success_person.csv', 'wb')
    wrtr_success = csv.writer(person_success_file, delimiter=',', quotechar='"')
    wrtr_success.writerow(["Entry No.", "Person Name"])

    csvfile = open(file, 'rb')
    rows_persons = csv.DictReader(csvfile)
    
    i = 0
    for row in rows_persons:
        i = i + 1
        try:
            person_name = ' '.join([str(row['Member_Name']), str(row['Member_Surname'])]) 
            father_name = ' '.join([str(row['Husband_Father_Name']), 
                                    str(row['Husband_Father_Surname'])]) 
                                               
            person = Person(user_created_id = user_id.id,
                            partner_id = user_id.partner.id,
                            person_name = person_name,
                            father_name = father_name, 
                            village_id = village_map[row['Village_Name']], 
                            group_id = group_map[row['Shg_Name']+row['Village_Name']],
                            gender = 'F')
            
            person.save()
            wrtr_success.writerow([i, person_name])
            person_success_file.flush()
            print 'pushing', row['Member_Name']
        
        except Exception as e:
            ERROR += 1
            wrtr.writerow([i,person_name, e])
        person_errors_file.flush()

    person_errors_file.close()
    person_success_file.close()
    ERROR_FILENAMES.append(file_name_list+'_errors_person.csv')
    SUCCESS_FILENAMES.append(file_name_list + '_success_person.csv')
    