from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import csv

from dashboard.models import Person

csvfile_updated = open('path/scripts/List_updated.csv', 'rb')
csvfile_original = open('path/scripts/List.csv', 'rb')
csvfile_write = open('path/scripts/Deleted.csv', 'wb')

rows_updated = csv.DictReader(csvfile_updated)
rows_original = csv.DictReader(csvfile_original)

deleted = csv.DictWriter(csvfile_write, delimiter=',', fieldnames=rows_updated.fieldnames)
count_correct = 0
count_incorrect = 0
for row in rows_updated:
    try:
        person = Person.objects.get(id=row['DELETE_ID'])
        person.delete()
        count_correct += 1
        deleted.writerow(row)
    except (Person.DoesNotExist, ValueError), e:
        print row['DELETE_ID']
        print e
        count_incorrect += 1

for row in rows_original:
    try:
        person = Person.objects.get(id=row['DELETE_ID'])
        person.delete()
        count_correct += 1
        deleted.writerow(row)
    except (Person.DoesNotExist, ValueError), e:
        print row['DELETE_ID']
        print e
        count_incorrect += 1

print "Person Deleted: %s" % count_correct
print "Person Not Deleted: %s" % count_incorrect
csvfile_updated.close()
csvfile_original.close()
csvfile_write.close()
