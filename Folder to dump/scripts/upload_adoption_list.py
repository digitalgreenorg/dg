import csv, datetime

from django.core.management import setup_environ

import dg.settings
setup_environ(dg.settings)

from activities.models import  PersonAdoptPractice
from people.models import Person

csvfile = open("Adoption.csv", "rb")
csv_data = csv.reader(csvfile)

csv_file = open('op.csv', 'wb')
a = csv.writer(csv_file)
a.writerow(["Did not attend the screening"])

csv_data.next()
videos = []
for row in csv_data:
    if row[0]:
        for pma in Person.objects.get(id=row[0]).personmeetingattendance_set.all():
            for vid in pma.screening.videoes_screened.all():
                videos.append(str(vid.id))
    row[1] = datetime.datetime.strptime(row[1], "%d-%b-%y").strftime("20%y-%m-%d")
    try:
        if(row[2] in videos):
            c = PersonAdoptPractice(person_id=int(row[0]), video_id=int(row[2]), date_of_adoption=row[1], partner_id="13", user_created_id="1")
            c.save()
        else:
            a.writerow(row)
    except Exception, err:
        a.writerow([str(err)])

csvfile.close()
csv_file.close()
