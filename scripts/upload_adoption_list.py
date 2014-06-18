import csv

from django.core.management import setup_environ

import dg.settings
setup_environ(dg.settings)

from activities.models import  PersonAdoptPractice, PersonMeetingAttendance
from people.models import Person

csvfile = open("Adoption.csv", "rb")
csv_data = csv.reader(csvfile)

csvfle= open('op.csv', 'wb') 
a = csv.writer(csvfle)
a.writerow(["Did not attend the screening"])

csv_data.next()
videos = []
for row in csv_data:

	if row[0]:
		for pma in Person.objects.get(id = row[0]).personmeetingattendance_set.all():
			for vid in pma.screening.videoes_screened.all():
				videos.append(vid.id)
	try:

		if(row[2] in videos):
			
			c=PersonAdoptPractice(person_id=int(row[0]), video_id=int(row[2]), date_of_adoption=row[1])
			c.save()
		else:
			a.writerow(row)
			
	except Exception, err:
		a.writerow(str(err))
	
csvfile.close()
csvfle.close()

    	

	
	
	





