# Functions which create querystring which can be posted to the digital GREEN API.

def create_formq_string_for_screening(row,local_db):
	screening_data=row
	videos_screened = local_db.get_videos_screened_in_screening(row[0])
	farmer_groups = local_db.get_farmer_group_targeted_in_screening(row[0])
	formq_string="date="+screening_data[1]+"&start_time="+screening_data[2]+"&end_time="+screening_data[3]+\
	"&location="+screening_data[4]+"&village="+str(screening_data[8])+"&animator="+str(screening_data[10])
	for video in videos_screened: 
		formq_string+="&videoes_screened="+str(video[0])
	for grp in farmer_groups:
		formq_string+="&farmer_groups_targeted="+str(grp[0])
	formq_string+="&id="+str(row[0])
	#print formq_string
	return formq_string
	
	
def create_formq_string_for_adoption(row):
	adoption_data=row
	formq_string = "person="+str(adoption_data[1])+"&video="+str(adoption_data[2])+"&date_of_adoption="+adoption_data[4]+"&id="+str(row[0])+"&id="+str(row[0])
	return formq_string


def create_formq_string_for_attendance(row):
	formq_string = "person="+str(row[2])+"&interested="+str(row[3])+"&id="+str(row[0])+"&screening="+str(row[1])
	return formq_string


def create_formq_string_for_animator(row):
	addr =row[8]
	if(addr==None):
		addr =""
	age = str(row[2])
	if(age=="None"):
		age=""	
	values={'name':str(row[1]),'age':str(age),'gender':str(row[3]),'csp_flag':str(row[4]),'camera_operator_flag':str(row[5]),'facilitator_flag':str(row[6]),'address':addr,'partner':str(row[9]),'id':str(row[0]),'village':str(row[10])}
	formq_string = urllib.urlencode(values)
	return formq_string

def create_formq_string_for_animator_assigned_villages(row):
	formq_string = "village="+str(row[2])+"&id="+str(row[0])+"&animator="+str(row[1])
	return formq_string

def create_formq_string_for_person_groups(row):
	formq_string ="group_name="+str(row[1])+"&village="+str(row[5])+"&id="+str(row[0])
	return formq_string

def create_formq_string_for_person(row):
	addr =row[6]
	if(addr==None):
		addr =""
	age = str(row[3])
	if(age=="None"):
		age=""
	formq_string = "person_name="+str(row[1])+"&father_name="+str(row[2])+"&age="+age+"&gender="+str(row[4])+"&address="+addr+"&village="+str(row[8])+"&id="+str(row[0])+"&group="+str(row[9])
	return formq_string
