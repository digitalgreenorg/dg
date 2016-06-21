from django.contrib.auth.models import User
from django.db import models

from activities.models import PersonMeetingAttendance, Screening, PersonAdoptPractice
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from dashboard.forms import CocoUserForm
from videos.models import  NonNegotiable,Video

FOREIGN_KEYS={
	'animator': {
			Screening: 'animator' ,
			AnimatorAssignedVillage : 'animator'
			}
}
