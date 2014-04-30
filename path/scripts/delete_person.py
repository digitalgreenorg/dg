from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import csv

from people.models import Person

csvfile = open('path/scripts/List.csv', 'rb')
csvfile_write = open('path/scripts/Not Deleted.csv', 'wb')

rows = csv.DictReader(csvfile)
not_deleted = csv.DictWriter(csvfile_write, delimiter=',', fieldnames=rows.fieldnames)
count_correct = 0
count_incorrect = 0
for row in rows:
    try:
        person = Person.objects.get(person_name=row['PERSON_NAME'], father_name=row['FATHER_NAME'], village__village_name=row['VILLAGE_NAME'])
        person.delete()
        count_correct += 1
    except Person.DoesNotExist, e:
        not_deleted.writerow(row)
        count_incorrect += 1

print "Person Deleted: %s" % count_correct
print "Person Not Deleted: %s" % count_incorrect
csvfile.close()
csvfile_write.close()
