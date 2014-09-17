import os.path, dg.settings

from django.core.management import setup_environ
setup_environ(dg.settings)
from geographies.models import Village, Block
from people.models import PersonGroup, Person
from coco.models import CocoUser
import csv

ERROR=0 #variable to identify if any error occurs in uploaded file
ERROR_FILENAMES = [] #contains the files to be zipped for download
SUCCESS_FILENAMES = []

def add_person(file, user_id, block_id):
    
    file = os.path.join(dg.settings.MEDIA_ROOT, file)
    
    csvfile = open(file, 'rb')
    rows = csv.DictReader(csvfile)    
    req_field = ['Village_Name','Shg_Name','Member_Name','Member_Surname','Husband_Father_Name','Husband_Father_Surname']
    for row in rows:
        if set(req_field)==set(row.keys()) and len(req_field)==len(row.keys()):
            execute_upoad(file, user_id, block_id)
            break
        else:
            prevent_execution = 1
            return prevent_execution
            
  
def execute_upoad(file, user_id, block_id):
    global ERROR
    
    user_id = CocoUser.objects.get(user__id=user_id)
    block_id = Block.objects.get(id=block_id)
        
    village_errors_file = open(os.path.splitext(file)[0]+'_village_errors.csv', 'wb')
    wrtr = csv.writer(village_errors_file, delimiter=',', quotechar='"')
    
    village_success_file =open(os.path.splitext(file)[0]+'_village_success.csv', 'wb')
    wrtr_success = csv.writer(village_success_file, delimiter=',', quotechar='"')
    
    csvfile = open(file, 'rb')
    rows = csv.DictReader(csvfile)
        
    village_querry_set = Village.objects.values('village_name','id')
    village_map = dict(village_querry_set)
    
    i = 0
    error_villages = []
    
    for row in rows:
        if str(row['Village_Name']) not in village_map:
            print "village"
            village_name = str(row['Village_Name'])
            
            try:
                i = i + 1
                print i
                village = Village(user_created_id = user_id.id, 
                                  village_name = row['Village_Name'], 
                                  block_id = block_id.id)
                
                village.save()
                village_map[row['Village_Name']] = village.id
                wrtr_success.writerow([row['Village_Name']])
                village_success_file.flush()
                print 'pushing', row['Village_Name']
            
            except Exception as e:
                ERROR += 1
                if village_name not in error_villages:
                    wrtr.writerow([row['Village_Name'], e])
                    error_villages.append(village_name)
                village_errors_file.flush()
    
    village_success_file.close()
    village_errors_file.close()
    
    ERROR_FILENAMES.append(str(os.path.splitext(file)[0].split('/')[-1]+'_village_errors.csv'))
    SUCCESS_FILENAMES.append(str(os.path.splitext(file)[0].split('/')[-1]+'_village_success.csv'))
    
    group_errors_file = open(os.path.splitext(file)[0]+'_group_errors.csv', 'wb')
    wrtr = csv.writer(group_errors_file, delimiter=',', quotechar='"')
    
    group_success_file = open(os.path.splitext(file)[0]+'_group_success.csv', 'wb')
    wrtr_success = csv.writer(group_success_file, delimiter=',', quotechar='"')

    csvfile = open(file, 'rb')
    rows2 = csv.DictReader(csvfile)

    group_querry_set = PersonGroup.objects.values('group_name','id')
    group_map = dict(group_querry_set)
    
    i = 0
    error_group = []
    for row in rows2:
        if str(row['Shg_Name']) + str(row['Village_Name']) not in group_map:
            print "group"
            try:
                i = i + 1
                print i
                group_name = str(row['Shg_Name'])
               

                group = PersonGroup(user_created_id = user_id.id,
                                    partner_id = user_id.partner.id,
                                    group_name = row['Shg_Name'], 
                                    village_id = village_map[row['Village_Name']])
                group.save()
                group_map[row['Shg_Name'] + row['Village_Name']] = group.id
                wrtr_success.writerow([row['Shg_Name']])
                group_success_file.flush()
                print 'pushing', row['Shg_Name']
            
            except Exception as e:
                ERROR += 1
                if group_name not in error_group:
                    wrtr.writerow([row['Shg_Name'], e] )
                    error_group.append(group_name)
                group_errors_file.flush()

    group_errors_file.close()
    group_success_file.close()
    
    ERROR_FILENAMES.append(str(os.path.splitext(file)[0].split('/')[-1]+'_group_errors.csv'))      
    SUCCESS_FILENAMES.append(str(os.path.splitext(file)[0].split('/')[-1]+'_group_success.csv'))
        
    person_errors_file = open(os.path.splitext(file)[0]+'_person_errors.csv', 'wb')
    wrtr = csv.writer(person_errors_file, delimiter=',', quotechar='"')
    
    person_success_file = open(os.path.splitext(file)[0]+'_person_success.csv', 'wb')
    wrtr_success = csv.writer(person_success_file, delimiter=',', quotechar='"')

    csvfile = open(file, 'rb')
    rows2 = csv.DictReader(csvfile)

    i = 0
    for row in rows2:
        print "person"
        try:
            i = i + 1
            print i
            person = Person(user_created_id = user_id.id, partner_id = user_id.partner.id, person_name = ' '.join([row['Member_Name'], row['Member_Surname']]), 
                             father_name = ' '.join([row['Husband_Father_Name'], row['Husband_Father_Surname']]), 
                             village_id = village_map[row['Village_Name']], group_id = group_map[row['Shg_Name']+ row['Village_Name']],
                             gender = 'F')
            person.save()
            wrtr_success.writerow([''.join([str(row['Member_Name ']),str(row['Member_Surname'])])])
            person_success_file.flush()
            print 'pushing', row['Member_Name']
        
        except Exception as e:
            ERROR += 1
            
            wrtr.writerow([' '.join([str(row['Member_Name']),str(row['Member_Surname'])]), e])
            person_errors_file.flush()

    person_errors_file.close()
    person_success_file.close()
    ERROR_FILENAMES.append(str(os.path.splitext(file)[0].split('/')[-1]+'_person_errors.csv'))
    SUCCESS_FILENAMES.append(str(os.path.splitext(file)[0].split('/')[-1]+'_person_success.csv'))
    