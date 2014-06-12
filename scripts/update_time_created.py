from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from activities.models import PersonMeetingAttendance, PersonAdoptPractice, Screening
from dashboard.models import Person as OldPerson, PersonAdoptPractice as OldAdoption, PersonMeetingAttendance as OldAttendance,  Screening as OldScreening
from people.models import Person


for adoption in PersonAdoptPractice.objects.exclude(old_coco_id__isnull=True):
    old_adoption = OldAdoption.objects.get(id=adoption.old_coco_id)
    adoption.time_created = old_adoption.time_created
    adoption.save()

print "Adoption Updated"

for screening in Screening.objects.exclude(old_coco_id__isnull=True):
    old_screening = OldScreening.objects.get(id=screening.old_coco_id)
    screening.time_created = old_screening.time_created
    screening.save()

print "Screening Updated"


for attend in PersonMeetingAttendance.objects.exclude(old_coco_id__isnull=True):
    old_attendance = OldAttendance.objects.get(id=attend.old_coco_id)
    attend.time_created = old_attendance.time_created
    attend.save()

print "Attendance Updated"


for person in Person.objects.exclude(old_coco_id__isnull=True):
    old_person = OldPerson.objects.get(id=person.old_coco_id_)
    person.time_created = old_person.time_created
    person.save()

print "Person Updated"

