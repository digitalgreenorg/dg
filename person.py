#from django.core.management import setup_environ322
from django.core.management import setup_environ
import site, sys
#sys.path.append('/home/ubuntu/code/dg_git')
import dg.settings
setup_environ(dg.settings)
from activities.models import PersonAdoptPractice
from geographies.models import Village, Block
from people.models import PersonGroup, Person
from coco.models import CocoUser
import csv, datetime

def add_person(file, id, block_id):

    blck= Block.objects.values_list('block_name').get(id=block_id)
    user_id = CocoUser.objects.get(user__id=id)
    
    village_errors_file = open('ib_village_errors.csv', 'wb')
    wrtr = csv.writer(village_errors_file, delimiter=',', quotechar='"')
    csvfile = open(file, 'rb')
    rows = csv.DictReader(csvfile)
  
    village_map1 = Village.objects.values('village_name','id')
    village_map = dict(village_map1)
    
    i = 0
    for row in rows:
        if row['village_name'] not in village_map:
            try:
                i = i + 1
                print i
                village = Village(user_created_id = user_id.id, village_name = row['village_name'], 
                              block_id = block_id)
                
                village.save()
                village_map[row['village_name']] = village.id
                print 'pushing', row['village_name']
            
            except Exception as e:
                wrtr.writerow([i, row['village_name'], e] )
                village_errors_file.flush()

    village_errors_file.close()

    group_errors_file = open('ib_group_errors.csv', 'wb')
    wrtr = csv.writer(group_errors_file, delimiter=',', quotechar='"')
    csvfile = open(file, 'rb')
    rows2 = csv.DictReader(csvfile)

    group_map1 = PersonGroup.objects.values('group_name','id')
    group_map = dict(group_map1)
    
    i = 0
    for row in rows2:
        if row['shg_name'] + row['village_name'] not in group_map:
            try:
                i = i + 1
                print i
                group = PersonGroup(user_created_id = user_id.id, partner_id = user_id.partner.id, group_name = row['shg_name'], 
                                 village_id = village_map[row['village_name']])
                group.save()
                group_map[row['shg_name'] + row['village_name']] = group.id
                print 'pushing', row['shg_name']
            
            except Exception as e:
                wrtr.writerow([i, row['shg_name'], e] )
                group_errors_file.flush()

    group_errors_file.close()      
        
    person_errors_file = open('ib_person_errors.csv', 'wb')
    wrtr = csv.writer(person_errors_file, delimiter=',', quotechar='"')
    csvfile = open(file, 'rb')
    rows2 = csv.DictReader(csvfile)

    i=0
    for row in rows2:
        try:
            i = i + 1
            print i
            person = Person(user_created_id = user_id.id, partner_id = user_id.partner.id, person_name = ' '.join([row['Member_Name'], row['Member_Surname']]), 
                             father_name = ' '.join([row['Husband_Father_Name'], row['Husband_Father_Surname']]), 
                             village_id = village_map[row['village_name']], group_id = group_map[row['shg_name']+ row['village_name']],
                             gender = 'F')
            person.save()
            print 'pushing', row['Member_Name']
        
        except Exception as e:
            wrtr.writerow([i, row['Member_Name'],row, e] )
            person_errors_file.flush()

    person_errors_file.close()

    


def main():
    add_person(sys.argv[1],35,485)


if __name__ == '__main__':
    main()