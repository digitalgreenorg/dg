from django.core.exceptions import ObjectDoesNotExist
import dashboard.models
import sqlite3
from create_querystring import *

SCREENING_TABLE_ID = 29
screening_table = {
	'table_name_in_local_db': "screening",
	'table_id': SCREENING_TABLE_ID,
	'table_name_in_online_db': "Screening",
	'pickle_file': 'screening_data',
	'create_formq_string':create_formq_string_for_screening,
	'add_url': "/dashboard/savescreeningoffline/"
}

person_adopt_practice_table = {
	'table_name_in_local_db': "person_adopt_practice",
	'table_id': 31,
	'table_name_in_online_db': "PersonAdoptPractice",
	'pickle_file': 'adoption_data',
	'create_formq_string':create_formq_string_for_adoption,
	'add_url': "/dashboard/savepersonadoptpracticeoffline/"
}

videos_table={
	'table_name_in_local_db': "video",
	'table_id': 27,
	'table_name_in_online_db': "Video",
	'pickle_file': 'video_data',
	'create_formq_string':'create_formq_string_for_screening',
	'add_url': "/dashboard/savescreeningoffline/"
}

villages_table={
	'table_name_in_local_db': "village",
	'table_id': 17,
	'table_name_in_online_db': "Village",
	'pickle_file': 'village_data',
	'create_formq_string':'create_formq_string_for_screening',
	'add_url': "/dashboard/savescreeningoffline/"
}

animators_table={
	'table_name_in_local_db': "animator",
	'table_id': 22,
	'table_name_in_online_db': "Animator",
	'pickle_file': 'animator_data',
	'create_formq_string':create_formq_string_for_animator,
	'add_url': "/dashboard/saveanimatoroffline/"
}

animator_assigned_villages_table={
	'table_name_in_local_db': "animator_assigned_village",
	'table_id': 24,
	'table_name_in_online_db': "AnimatorAssignedVillage",
	'pickle_file': 'animator_assigned_village_data',
	'create_formq_string':create_formq_string_for_animator_assigned_villages,
	'add_url': "/dashboard/saveanimatorassignedvillageoffline/"
}

person_groups_table={
	'table_name_in_local_db': "person_groups",
	'table_id': 19,
	'table_name_in_online_db': "PersonGroups",
	'pickle_file': 'person_groups_data',
	'create_formq_string':create_formq_string_for_person_groups,
	'add_url': "/dashboard/savepersongroupoffline/"
}

person_table= {
	'table_name_in_local_db': "person",
	'table_id': 20,
	'table_name_in_online_db': "Person",
	'pickle_file': 'person_data',
	'create_formq_string':create_formq_string_for_person,
	'add_url': "/dashboard/savepersonoffline/"
}

farmer_groups_targeted_table={
	'table_name_in_local_db': "screening_farmer_groups_targeted",
	'table_id': 40,
	'table_name_in_online_db': "GroupsTargetedInScreening",
	'pickle_file': 'farme_groups_targeted_data',
	#'create_formq_string':'create_formq_string_for_screening',
	#'add_url': "/dashboard/savescreeningoffline/"
}

screening_videos_screened_table={
	'table_name_in_local_db': "screening_videos_screened",
	'table_id': 41,
	'table_name_in_online_db': "VideosScreenedInScreening",
	'pickle_file': 'screening_videos_screened_data',
	#'create_formq_string':'create_formq_string_for_screening',
	#'add_url': "/dashboard/savescreeningoffline/"
}

person_meeting_attendance_table={
	'table_name_in_local_db': "person_meeting_attendance",
	'table_id': 30,
	'table_name_in_online_db': "PersonMeetingAttendance",
	'pickle_file': 'person_meeting_attendance',
	'create_formq_string':create_formq_string_for_attendance,
	'add_url': "/dashboard/savepersonmeetingattendanceoffline/"
}

check_tables = [animators_table,animator_assigned_villages_table,person_groups_table,screening_table,person_adopt_practice_table,person_table,\
videos_table,villages_table,]

class AccessLocalDb:
	cur=None
	con=None
	all_screenings=None
	use_local_db=None
	check_table=None

	def __init__(self,local_db_name,check_table_dict):
		#self.use_local_db = local_db_name
		self.con = sqlite3.connect(local_db_name)
		self.cur = self.con.cursor()
		self.check_table=check_table_dict
		self.all_screenings = self.cur.execute("select id from %s "% (self.check_table['table_name_in_local_db']))

	def get_next_id(self):
		return self.all_screenings.fetchone()
			
	def id_exists_in_formQ(self,s_id):
		#con2 = sqlite3.connect("C:\\Users\\hp\\Desktop\\digital Green\\digitalgreendatabase_2012_06_13_hardur.sqlite")
		cur2 = self.con.cursor()
		cur2.execute("select Count(*) from formqueue WHERE table_id='%d' AND global_pk_id='%d'" % (self.check_table['table_id'],s_id))
		if (cur2.fetchone()[0]==0):
			return False
		return True
		
	def id_sync_status(self,s_id):
		#con2 = sqlite3.connect("C:\\Users\\hp\\Desktop\\digital Green\\digitalgreendatabase_2012_06_13_hardur.sqlite")
		cur2 = self.con.cursor()
		#cur2.execute("select Count(*) from formqueue WHERE table_id='%d' AND global_pk_id='%d'" % (29,s_id))
		cur2.execute("select sync_status from formqueue WHERE table_id='%d' AND global_pk_id='%d'" % (self.check_table['table_id'],s_id))
		return cur2.fetchone()[0]
	
	def get_user(self):
		cur2 = self.con.cursor()
		cur2.execute("select username from user ")
		return cur2.fetchone()[0]

	def get_videos_screened_in_screening(self,s_id):
		cur2 = self.con.cursor()
		cur2.execute("select video_id from screening_videos_screened WHERE screening_id=%d" % (s_id))
		return cur2.fetchall()
    
	def get_farmer_group_targeted_in_screening(self,s_id):
		cur2 = self.con.cursor()
		cur2.execute("select persongroups_id from screening_farmer_groups_targeted WHERE screening_id=%d" % (s_id))
		return cur2.fetchall()
    
	def get_table_data_by_id(self,s_id):
		cur2 = self.con.cursor()
		cur2.execute("select * from %s WHERE id=%d" % (self.check_table['table_name_in_local_db'],s_id))
		return cur2.fetchone()
		
	def get_screening_attendance(self,s_id):
		cur2 = self.con.cursor()
		cur2.execute("select * from person_meeting_attendance WHERE screening_id=%d" % (s_id))
		return cur2.fetchall()

class AccessOnlineDb:
	def id_exists(self,s_id,table_name_in_online_db):
		try:
			table=getattr(dashboard.models,table_name_in_online_db)
			table.objects.get(id=s_id)
		except ObjectDoesNotExist:
			return False
		else:
			return True
