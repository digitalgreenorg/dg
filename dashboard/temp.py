# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

# Variables
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Region(models.Model):
    region_id = models.IntegerField(primary_key=True, db_column='REGION_ID') # Field name made lowercase.
    region_name = models.CharField(max_length=100, db_column='REGION_NAME') # Field name made lowercase.
    start_date = models.DateField(null=True, db_column='START_DATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'REGION'

class EquipmentHolder(models.Model):
    equipmentholder_id = models.IntegerField(primary_key=True, db_column='EQUIPMENTHOLDER_ID') # Field name made lowercase.
    class Meta:
        db_table = u'EQUIPMENT_HOLDER'

class Reviewer(models.Model):
    reviewer_id = models.IntegerField(primary_key=True, db_column='REVIEWER_ID') # Field name made lowercase.
    reviewer_name = models.CharField(max_length=100, db_column='REVIEWER_NAME') # Field name made lowercase.
    reviewer_comments = models.TextField(db_column='REVIEWER_COMMENTS', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'REVIEWER'

class DevelopmentManager(models.Model):
    dm_id = models.IntegerField(primary_key=True, db_column='DM_ID') # Field name made lowercase.
    name = models.CharField(max_length=100, db_column='NAME') # Field name made lowercase.
    age = models.IntegerField(max_length=3,null=True, db_column='AGE', blank=True) # Field name made lowercase.
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER') # Field name made lowercase.
    hire_date = models.DateField(null=True, db_column='HIRE_DATE', blank=True) # Field name made lowercase.
    phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=500, db_column='ADDRESS', blank=True) # Field name made lowercase.
    speciality = models.TextField(db_column='SPECIALITY', blank=True) # Field name made lowercase.
    region = models.ForeignKey(Region) #null=True, db_column='REGION_ID', blank=True) # Field name made lowercase.
    start_day = models.DateField(null=True, db_column='START_DAY', blank=True) # Field name made lowercase.
    reviewer = models.ForeignKey(Reviewer) #(null=True, db_column='REVIEWER_ID', blank=True) # Field name made lowercase.
    equipmentholder = models.ForeignKey(EquipmentHolder) #IntegerField(null=True, db_column='EQUIPMENTHOLDER_ID', blank=True) # Field name made lowercase.
    salary = models.FloatField(null=True, db_column='SALARY', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'DEVELOPMENT_MANAGER'

class State(models.Model):
    state_id = models.IntegerField(primary_key=True, db_column='STATE_ID') # Field name made lowercase.
    state_name = models.CharField(max_length=100, db_column='STATE_NAME') # Field name made lowercase.
    region = models.ForeignKey(Region) #IntegerField(null=True, db_column='REGION_ID', blank=True) # Field name made lowercase.
    start_date = models.DateField(null=True, db_column='START_DATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'STATE'

class Partners(models.Model):
    partner_id = models.IntegerField(primary_key=True, db_column='PARTNER_ID') # Field name made lowercase.
    partner_name = models.CharField(max_length=100, db_column='PARTNER_NAME') # Field name made lowercase.
    date_of_association = models.DateField(null=True, db_column='DATE_OF_ASSOCIATION', blank=True) # Field name made lowercase.
    phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=500, db_column='ADDRESS', blank=True) # Field name made lowercase.
    reviewer = models.ForeignKey(Reviewer) #IntegerField(null=True, db_column='REVIEWER_ID', blank=True) # Field name made lowercase.
    equipmentholder = models.ForeignKey(EquipmentHolder) #IntegerField(null=True, db_column='EQUIPMENTHOLDER_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PARTNERS'

class FieldOfficer(models.Model):
    fieldofficer_id = models.IntegerField(primary_key=True, db_column='FIELDOFFICER_ID') # Field name made lowercase.
    name = models.CharField(max_length=100, db_column='NAME') # Field name made lowercase.
    age = models.IntegerField(max_length=3,null=True, db_column='AGE', blank=True) # Field name made lowercase.
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER') # Field name made lowercase.
    hire_date = models.DateField(null=True, db_column='HIRE_DATE', blank=True) # Field name made lowercase.
    salary = models.FloatField(null=True, db_column='SALARY', blank=True) # Field name made lowercase.
    phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=500, db_column='ADDRESS', blank=True) # Field name made lowercase.
    reviewer = models.ForeignKey(Reviewer) #IntegerField(null=True, db_column='REVIEWER_ID', blank=True) # Field name made lowercase.
    equipmentholder = models.ForeignKey(EquipmentHolder) #IntegerField(null=True, db_column='EQUIPMENTHOLDER_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'FIELD_OFFICER'

class Block(models.Model):
    block_id = models.IntegerField(primary_key=True, db_column='BLOCK_ID') # Field name made lowercase.
    block_name = models.CharField(max_length=100, db_column='BLOCK_NAME') # Field name made lowercase.
    start_date = models.DateField(null=True, db_column='START_DATE', blank=True) # Field name made lowercase.
    state = models.ForeignKey(State) #IntegerField(null=True, db_column='STATE_ID', blank=True) # Field name made lowercase.
    fieldofficer = models.ForeignKey(FieldOfficer) #IntegerField(null=True, db_column='FIELDOFFICER_ID', blank=True) # Field name made lowercase.
    fieldofficer_startday = models.DateField(null=True, db_column='FIELDOFFICER_STARTDAY', blank=True) # Field name made lowercase.
    partner = models.ForeignKey(Partners) #IntegerField(null=True, db_column='PARTNER_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'BLOCK'

class Village(models.Model):
    village_id = models.IntegerField(primary_key=True, db_column='VILLAGE_ID') # Field name made lowercase.
    village_name = models.CharField(max_length=100, db_column='VILLAGE_NAME') # Field name made lowercase.
    block = models.ForeignKey(Block) #IntegerField(null=True, db_column='BLOCK_ID', blank=True) # Field name made lowercase.
    no_of_households = models.IntegerField(null=True, db_column='NO_OF_HOUSEHOLDS', blank=True) # Field name made lowercase.
    population = models.IntegerField(null=True, db_column='POPULATION', blank=True) # Field name made lowercase.
    road_connectivity = models.CharField(max_length=100, db_column='ROAD_CONNECTIVITY', blank=True) # Field name made lowercase.
    control = models.NullBooleanField(null=True, db_column='CONTROL', blank=True) # Field name made lowercase.
    start_date = models.DateField(null=True, db_column='START_DATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'VILLAGE'

class MonthlyCostPerVillage(models.Model):
    village = models.ForeignKey(Village) # IntegerField(primary_key=True, db_column='VILLAGE_ID') # Field name made lowercase.
    date = models.DateField(db_column='DATE') # Field name made lowercase.
    labor_cost = models.FloatField(null=True, db_column='LABOR_COST', blank=True) # Field name made lowercase.
    equipment_cost = models.FloatField(null=True, db_column='EQUIPMENT_COST', blank=True) # Field name made lowercase.
    transportation_cost = models.FloatField(null=True, db_column='TRANSPORTATION_COST', blank=True) # Field name made lowercase.
    miscellaneous_cost = models.FloatField(null=True, db_column='MISCELLANEOUS_COST', blank=True) # Field name made lowercase.
    total_cost = models.FloatField(null=True, db_column='TOTAL_COST', blank=True) # Field name made lowercase.
    partners_cost = models.FloatField(null=True, db_column='PARTNERS_COST', blank=True) # Field name made lowercase.
    digitalgreen_cost = models.FloatField(null=True, db_column='DIGITALGREEN_COST', blank=True) # Field name made lowercase.
    community_cost = models.FloatField(null=True, db_column='COMMUNITY_COST', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'MONTHLY_COST_PER_VILLAGE'

class PersonGroups(models.Model):
    DAY_CHOICES = (
		('Monday','Monday'),
		('Tuesday','Tuesday'),
		('Wednesday','Wednesday'),
		('Thursday','Thursday'),
		('Friday','Friday'),
		('Saturday','Saturday'),
		('Sunday','Sunday'),
		  )
    group_identifier = models.IntegerField(primary_key=True, db_column='GROUP_IDENTIFIER') # Field name made lowercase.
    group_name = models.CharField(max_length=100, db_column='GROUP_NAME') # Field name made lowercase.
    days = models.CharField(max_length=9,choices=DAY_CHOICES, db_column='DAYS', blank=True) # Field name made lowercase.
    timings = models.TimeField(db_column='TIMINGS', blank=True) # Field name made lowercase. This field type is a guess.
    time_updated = models.DateTimeField(db_column='TIME_UPDATED') # Field name made lowercase.
    village = models.ForeignKey(Village) #IntegerField(null=True, db_column='VILLAGE_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PERSON_GROUPS'

class Person(models.Model):
    person_id = models.IntegerField(primary_key=True, db_column='PERSON_ID') # Field name made lowercase.
    person_name = models.CharField(max_length=100, db_column='PERSON_NAME') # Field name made lowercase.
    father_name = models.CharField(max_length=100, db_column='FATHER_NAME', blank=True) # Field name made lowercase.
    age = models.IntegerField(max_length=3, null=True, db_column='AGE', blank=True) # Field name made lowercase.
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER') # Field name made lowercase.
    phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=500, db_column='ADDRESS', blank=True) # Field name made lowercase.
    land_holdings = models.IntegerField(null=True, db_column='LAND_HOLDINGS', blank=True) # Field name made lowercase.
    village = models.ForeignKey(Village) #IntegerField(null=True, db_column='VILLAGE_ID', blank=True) # Field name made lowercase.
    group = models.ForeignKey(PersonGroups) #IntegerField(null=True, db_column='GROUP_IDENTIFIER', blank=True) # Field name made lowercase.
    equipmentholder = models.ForeignKey(EquipmentHolder) #IntegerField(null=True, db_column='EQUIPMENTHOLDER_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PERSON'

class PersonRelations(models.Model):
    person = models.ForeignKey(Person,related_name='person') #IntegerField(primary_key=True, db_column='PERSON_ID') # Field name made lowercase.
    relative = models.ForeignKey(Person,related_name='relative') #IntegerField(db_column='RELATIVE_ID') # Field name made lowercase.
    type_of_relationship = models.CharField(max_length=100, db_column='TYPE_OF_RELATIONSHIP') # Field name made lowercase.
    class Meta:
        db_table = u'PERSON_RELATIONS'

class Animator(models.Model):
    animator_id = models.IntegerField(primary_key=True, db_column='ANIMATOR_ID') # Field name made lowercase.
    name = models.CharField(max_length=100, db_column='NAME') # Field name made lowercase.
    age = models.IntegerField(max_length=3,null=True, db_column='AGE', blank=True) # Field name made lowercase.
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, db_column='GENDER') # Field name made lowercase.
    csp_flag = models.NullBooleanField(null=True, db_column='CSP_FLAG', blank=True) # Field name made lowercase.
    camera_operator_flag = models.NullBooleanField(null=True, db_column='CAMERA_OPERATOR_FLAG', blank=True) # Field name made lowercase.
    facilitator_flag = models.NullBooleanField(null=True, db_column='FACILITATOR_FLAG', blank=True) # Field name made lowercase.
    phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True) # Field name made lowercase.
    address = models.CharField(max_length=500, db_column='ADDRESS', blank=True) # Field name made lowercase.
    partner = models.ForeignKey(Partners) #IntegerField(null=True, db_column='PARTNER_ID', blank=True) # Field name made lowercase.
    homevillage = models.ForeignKey(Village) #IntegerField(null=True, db_column='HOMEVILLAGE_ID', blank=True) # Field name made lowercase.
    equipmentholder = models.ForeignKey(EquipmentHolder) #IntegerField(null=True, db_column='EQUIPMENTHOLDER_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'ANIMATOR'

class Training(models.Model):
    training_id = models.IntegerField(primary_key=True, db_column='TRAINING_ID') # Field name made lowercase.
    training_purpose = models.TextField(db_column='TRAINING_PURPOSE', blank=True) # Field name made lowercase.
    training_outcome = models.TextField(db_column='TRAINING_OUTCOME', blank=True) # Field name made lowercase.
    training_start_date = models.DateField(null=True, db_column='TRAINING_START_DATE', blank=True) # Field name made lowercase.
    training_end_date = models.DateField(null=True, db_column='TRAINING_END_DATE', blank=True) # Field name made lowercase.
    village = models.ForeignKey(Village) #IntegerField(db_column='VILLAGE_ID') # Field name made lowercase.
    dm = models.ForeignKey(DevelopmentManager) #IntegerField(db_column='DM_ID') # Field name made lowercase.
    fieldofficer = models.ForeignKey(FieldOfficer) #IntegerField(db_column='FIELDOFFICER_ID') # Field name made lowercase.
    class Meta:
        db_table = u'TRAINING'

class AnimatorTraining(models.Model):
    animator = models.ForeignKey(Animator) #IntegerField(primary_key=True, db_column='ANIMATOR_ID') # Field name made lowercase.
    training = models.ForeignKey(Training) #IntegerField(db_column='TRAINING_ID') # Field name made lowercase.
    class Meta:
        db_table = u'ANIMATOR_TRAINING'


class AnimatorAssignedVillage(models.Model):
    animator = models.ForeignKey(Animator) #IntegerField(primary_key=True, db_column='ANIMATOR_ID') # Field name made lowercase.
    village = models.ForeignKey(Village) #IntegerField(db_column='VILLAGE_ID') # Field name made lowercase.
    start_date = models.DateField(null=True, db_column='START_DATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'ANIMATOR_ASSIGNED_VILLAGE'

class AnimatorSalaryPerMonth(models.Model):
    animator = models.ForeignKey(Animator) #IntegerField(primary_key=True, db_column='ANIMATOR_ID') # Field name made lowercase.
    date = models.DateField(db_column='DATE') # Field name made lowercase.
    total_salary = models.FloatField(null=True, db_column='TOTAL_SALARY', blank=True) # Field name made lowercase.
    pay_date = models.DateField(null=True, db_column='PAY_DATE', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'ANIMATOR_SALARY_PER_MONTH'

class Video(models.Model):
    video_id = models.IntegerField(primary_key=True, db_column='VIDEO_ID') # Field name made lowercase.
    title = models.CharField(max_length=200, db_column='TITLE') # Field name made lowercase.
    duration = models.TimeField(null=True, db_column='DURATION', blank=True) # Field name made lowercase. This field type is a guess.
    language = models.CharField(max_length=100, db_column='LANGUAGE', blank=True) # Field name made lowercase.
    summary = models.TextField(db_column='SUMMARY', blank=True) # Field name made lowercase.
    picture_quality = models.CharField(max_length=200, db_column='PICTURE_QUALITY', blank=True) # Field name made lowercase.
    audio_quality = models.CharField(max_length=200, db_column='AUDIO_QUALITY', blank=True) # Field name made lowercase.
    editing_quality = models.CharField(max_length=200, db_column='EDITING_QUALITY', blank=True) # Field name made lowercase.
    thematic_quality = models.CharField(max_length=200, db_column='THEMATIC_QUALITY', blank=True) # Field name made lowercase.
    video_production_start_date = models.DateField(null=True, db_column='VIDEO_PRODUCTION_START_DATE', blank=True) # Field name made lowercase.
    video_production_end_date = models.DateField(null=True, db_column='VIDEO_PRODUCTION_END_DATE', blank=True) # Field name made lowercase.
    storyboard_filename = models.FileField(upload_to='storyboard', db_column='STORYBOARD_FILENAME', blank=True) # Field name made lowercase.
    raw_filename = models.FileField(upload_to='rawfile', db_column='RAW_FILENAME', blank=True) # Field name made lowercase.
    movie_maker_project_filename = models.FileField(upload_to='movie_maker_project_file', db_column='MOVIE_MAKER_PROJECT_FILENAME', blank=True) # Field name made lowercase.
    final_edited_filename = models.FileField(upload_to='final_edited_file', db_column='FINAL_EDITED_FILENAME', blank=True) # Field name made lowercase.
    village = models.ForeignKey(Village) #IntegerField(null=True, db_column='VILLAGE_ID', blank=True) # Field name made lowercase.
    facilitator = models.ForeignKey(Animator,related_name='facilitator') #IntegerField(null=True, db_column='FACILITATOR_ID', blank=True) # Field name made lowercase.
    cameraoperator = models.ForeignKey(Animator,related_name='cameraoperator') #IntegerField(null=True, db_column='CAMERAOPERATOR_ID', blank=True) # Field name made lowercase.
    reviewer = models.ForeignKey(Reviewer) #IntegerField(null=True, db_column='REVIEWER_ID', blank=True) # Field name made lowercase.
    supplementary_video_produced = models.ForeignKey('self') #IntegerField(null=True, db_column='SUPPLEMENTARY_VIDEO_PRODUCED', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'VIDEO'

class Practices(models.Model):
    practice_id = models.IntegerField(primary_key=True, db_column='PRACTICE_ID') # Field name made lowercase.
    practice_name = models.CharField(max_length=200, db_column='PRACTICE_NAME') # Field name made lowercase.
    seasonality = models.CharField(max_length=200, db_column='SEASONALITY', blank=True) # Field name made lowercase.
    summary = models.TextField(db_column='SUMMARY', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PRACTICES'

class VideoReleatedToPractice(models.Model):
    video = models.ForeignKey(Video) #IntegerField(primary_key=True, db_column='VIDEO_ID') # Field name made lowercase.
    practice = models.ForeignKey(Practices) #IntegerField(db_column='PRACTICE_ID') # Field name made lowercase.
    class Meta:
        db_table = u'VIDEO_RELEATED_TO_PRACTICE'

class PersonDisplayedInVideo(models.Model):
    video = models.ForeignKey(Video) #IntegerField(primary_key=True, db_column='VIDEO_ID') # Field name made lowercase.
    person = models.ForeignKey(Person) #IntegerField(db_column='PERSON_ID') # Field name made lowercase.
    class Meta:
        db_table = u'PERSON_DISPLAYED_IN_VIDEO'


class Screening(models.Model):
    screening_id = models.IntegerField(primary_key=True, db_column='SCREENING_ID') # Field name made lowercase.
    date = models.DateField(db_column='DATE') # Field name made lowercase.
    start_time = models.TimeField(db_column='START_TIME') # Field name made lowercase. This field type is a guess.
    end_time = models.TimeField(db_column='END_TIME') # Field name made lowercase. This field type is a guess.
    location = models.CharField(max_length=200, db_column='LOCATION', blank=True) # Field name made lowercase.
    topic = models.CharField(max_length=200, db_column='TOPIC', blank=True) # Field name made lowercase.
    target_person_attendance = models.IntegerField(null=True, db_column='TARGET_PERSON_ATTENDANCE', blank=True) # Field name made lowercase.
    target_audience_interest = models.IntegerField(null=True, db_column='TARGET_AUDIENCE_INTEREST', blank=True) # Field name made lowercase.
    target_adoptions = models.IntegerField(null=True, db_column='TARGET_ADOPTIONS', blank=True) # Field name made lowercase.
    village = models.ForeignKey(Village) #IntegerField(null=True, db_column='VILLAGE_ID', blank=True) # Field name made lowercase.
    fieldofficer = models.ForeignKey(FieldOfficer) #IntegerField(null=True, db_column='FIELDOFFICER_ID', blank=True) # Field name made lowercase.
    animator = models.ForeignKey(Animator) #IntegerField(null=True, db_column='ANIMATOR_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SCREENING'

class ScreeningPersongroup(models.Model):
    screening = models.ForeignKey(Screening) #IntegerField(primary_key=True, db_column='SCREENING_ID') # Field name made lowercase.
    group = models.ForeignKey(PersonGroups) #IntegerField(db_column='GROUP_IDENTIFIER') # Field name made lowercase.
    class Meta:
        db_table = u'SCREENING_PERSONGROUP'




class VideoScreenedInMeetings(models.Model):
    video = models.ForeignKey(Video) #IntegerField(primary_key=True, db_column='VIDEO_ID') # Field name made lowercase.
    screening = models.ForeignKey(Screening) #IntegerField(db_column='SCREENING_ID') # Field name made lowercase.
    class Meta:
        db_table = u'VIDEO_SCREENED_IN_MEETINGS'

class PersonMeetingAttendance(models.Model):
    screening = models.ForeignKey(Screening) #IntegerField(primary_key=True, db_column='SCREENING_ID') # Field name made lowercase.
    person = models.ForeignKey(Person) #IntegerField(db_column='PERSON_ID') # Field name made lowercase.
    expressed_interest_practice = models.ForeignKey(Practices,related_name='expressed_interest_practice') #IntegerField(null=True, db_column='EXPRESSED_INTEREST_PRACTICE_ID', blank=True) # Field name made lowercase.
    expressed_interest = models.TextField(db_column='EXPRESSED_INTEREST', blank=True) # Field name made lowercase.
    expressed_adoption_practice = models.ForeignKey(Practices,related_name='expressed_adoption_practice') #IntegerField(null=True, db_column='EXPRESSED_ADOPTION_PRACTICE_ID', blank=True) # Field name made lowercase.
    expressed_adoption = models.TextField(db_column='EXPRESSED_ADOPTION', blank=True) # Field name made lowercase.
    expressed_question_practice = models.ForeignKey(Practices,related_name='expressed_question_practice') #IntegerField(null=True, db_column='EXPRESSED_QUESTION_PRACTICE_ID', blank=True) # Field name made lowercase.
    expressed_question = models.TextField(db_column='EXPRESSED_QUESTION', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PERSON_MEETING_ATTENDANCE'

class PersonAdoptPractice(models.Model):
    person = models.ForeignKey(Person) #IntegerField(primary_key=True, db_column='PERSON_ID') # Field name made lowercase.
    practice = models.ForeignKey(Practices) #IntegerField(db_column='PRACTICE_ID') # Field name made lowercase.
    prior_adoption_flag = models.NullBooleanField(null=True, db_column='PRIOR_ADOPTION_FLAG', blank=True) # Field name made lowercase.
    date_of_adoption = models.DateField(null=True, db_column='DATE_OF_ADOPTION', blank=True) # Field name made lowercase.
    quality = models.CharField(max_length=200, db_column='QUALITY', blank=True) # Field name made lowercase.
    quantity = models.IntegerField(null=True, db_column='QUANTITY', blank=True) # Field name made lowercase.
    quantity_unit = models.CharField(max_length=150, db_column='QUANTITY_UNIT', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PERSON_ADOPT_PRACTICE'

class EquipmentId(models.Model):
    equipment_id = models.IntegerField(primary_key=True, db_column='EQUIPMENT_ID') # Field name made lowercase.
    equipment_type = models.CharField(max_length=300, db_column='EQUIPMENT_TYPE') # Field name made lowercase.
    model_no = models.CharField(max_length=300, db_column='MODEL_NO', blank=True) # Field name made lowercase.
    serial_no = models.CharField(max_length=300, db_column='SERIAL_NO', blank=True) # Field name made lowercase.
    cost = models.FloatField(null=True, db_column='COST', blank=True) # Field name made lowercase.
    procurement_date = models.DateField(null=True, db_column='PROCUREMENT_DATE', blank=True) # Field name made lowercase.
    warranty_expiration_date = models.DateField(null=True, db_column='WARRANTY_EXPIRATION_DATE', blank=True) # Field name made lowercase.
    equipmentholder = models.ForeignKey(EquipmentHolder) #IntegerField(null=True, db_column='EQUIPMENTHOLDER_ID', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'EQUIPMENT_ID'
