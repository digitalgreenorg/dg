# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OfflineUser'
        db.create_table('dashboard_offlineuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('offline_pk_id', self.gf('dashboard.fields.PositiveBigIntegerField')()),
        ))
        db.send_create_signal('dashboard', ['OfflineUser'])

        # Adding model 'RegionTest'
        db.create_table(u'region_test', (
            ('region_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100, db_column='REGION_NAME')),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='id')),
        ))
        db.send_create_signal('dashboard', ['RegionTest'])

        # Adding model 'Region'
        db.create_table(u'region', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('region_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100, db_column='REGION_NAME')),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['Region'])

        # Adding model 'Country'
        db.create_table(u'country', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100, db_column='COUNTRY_NAME')),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['Country'])

        # Adding model 'EquipmentHolder'
        db.create_table(u'equipment_holder', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('dashboard.fields.PositiveBigIntegerField')()),
        ))
        db.send_create_signal('dashboard', ['EquipmentHolder'])

        # Adding model 'Reviewer'
        db.create_table(u'reviewer', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('dashboard.fields.PositiveBigIntegerField')()),
        ))
        db.send_create_signal('dashboard', ['Reviewer'])

        # Adding model 'DevelopmentManager'
        db.create_table(u'development_manager', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='NAME')),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, db_column='AGE', blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='GENDER')),
            ('hire_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='HIRE_DATE', blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PHONE_NO', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500, db_column='ADDRESS', blank=True)),
            ('speciality', self.gf('django.db.models.fields.TextField')(db_column='SPECIALITY', blank=True)),
            ('region', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Region'])),
            ('start_day', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DAY', blank=True)),
            ('salary', self.gf('django.db.models.fields.FloatField')(null=True, db_column='SALARY', blank=True)),
        ))
        db.send_create_signal('dashboard', ['DevelopmentManager'])

        # Adding model 'State'
        db.create_table(u'state', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('state_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100, db_column='STATE_NAME')),
            ('region', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Region'])),
            ('country', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Country'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['State'])

        # Adding model 'Partners'
        db.create_table(u'partners', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('partner_name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PARTNER_NAME')),
            ('date_of_association', self.gf('django.db.models.fields.DateField')(null=True, db_column='DATE_OF_ASSOCIATION', blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PHONE_NO', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500, db_column='ADDRESS', blank=True)),
        ))
        db.send_create_signal('dashboard', ['Partners'])

        # Adding model 'FieldOfficer'
        db.create_table(u'field_officer', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='NAME')),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, db_column='AGE', blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='GENDER')),
            ('hire_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='HIRE_DATE', blank=True)),
            ('salary', self.gf('django.db.models.fields.FloatField')(null=True, db_column='SALARY', blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PHONE_NO', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500, db_column='ADDRESS', blank=True)),
        ))
        db.send_create_signal('dashboard', ['FieldOfficer'])

        # Adding model 'District'
        db.create_table(u'district', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100, db_column='DISTRICT_NAME')),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
            ('state', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.State'])),
            ('fieldofficer', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.FieldOfficer'])),
            ('fieldofficer_startday', self.gf('django.db.models.fields.DateField')(null=True, db_column='FIELDOFFICER_STARTDAY', blank=True)),
            ('partner', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Partners'])),
        ))
        db.send_create_signal('dashboard', ['District'])

        # Adding model 'Block'
        db.create_table(u'block', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('block_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100, db_column='BLOCK_NAME')),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
            ('district', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.District'])),
        ))
        db.send_create_signal('dashboard', ['Block'])

        # Adding model 'Village'
        db.create_table(u'village', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('village_name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='VILLAGE_NAME')),
            ('block', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Block'])),
            ('no_of_households', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='NO_OF_HOUSEHOLDS', blank=True)),
            ('population', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='POPULATION', blank=True)),
            ('road_connectivity', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='ROAD_CONNECTIVITY', blank=True)),
            ('control', self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='CONTROL', blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Village'])

        # Adding unique constraint on 'Village', fields ['village_name', 'block']
        db.create_unique(u'village', ['VILLAGE_NAME', 'block_id'])

        # Adding model 'MonthlyCostPerVillage'
        db.create_table(u'monthly_cost_per_village', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_column='DATE')),
            ('labor_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='LABOR_COST', blank=True)),
            ('equipment_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='EQUIPMENT_COST', blank=True)),
            ('transportation_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='TRANSPORTATION_COST', blank=True)),
            ('miscellaneous_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='MISCELLANEOUS_COST', blank=True)),
            ('total_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='TOTAL_COST', blank=True)),
            ('partners_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='PARTNERS_COST', blank=True)),
            ('digitalgreen_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='DIGITALGREEN_COST', blank=True)),
            ('community_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='COMMUNITY_COST', blank=True)),
        ))
        db.send_create_signal('dashboard', ['MonthlyCostPerVillage'])

        # Adding model 'PersonGroups'
        db.create_table(u'person_groups', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='GROUP_NAME')),
            ('days', self.gf('django.db.models.fields.CharField')(max_length=9, db_column='DAYS', blank=True)),
            ('timings', self.gf('django.db.models.fields.TimeField')(null=True, db_column='TIMINGS', blank=True)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_column='TIME_UPDATED', blank=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
        ))
        db.send_create_signal('dashboard', ['PersonGroups'])

        # Adding unique constraint on 'PersonGroups', fields ['group_name', 'village']
        db.create_unique(u'person_groups', ['GROUP_NAME', 'village_id'])

        # Adding model 'Person'
        db.create_table(u'person', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PERSON_NAME')),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='FATHER_NAME', blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, db_column='AGE', blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='GENDER')),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PHONE_NO', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500, db_column='ADDRESS', blank=True)),
            ('land_holdings', self.gf('django.db.models.fields.FloatField')(null=True, db_column='LAND_HOLDINGS', blank=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('group', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.PersonGroups'], null=True, blank=True)),
            ('date_of_joining', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('image_exists', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dashboard', ['Person'])

        # Adding unique constraint on 'Person', fields ['person_name', 'father_name', 'group', 'village']
        db.create_unique(u'person', ['PERSON_NAME', 'FATHER_NAME', 'group_id', 'village_id'])

        # Adding model 'PersonRelations'
        db.create_table(u'person_relations', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('person', self.gf('dashboard.fields.BigForeignKey')(related_name='person', to=orm['dashboard.Person'])),
            ('relative', self.gf('dashboard.fields.BigForeignKey')(related_name='relative', to=orm['dashboard.Person'])),
            ('type_of_relationship', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='TYPE_OF_RELATIONSHIP')),
        ))
        db.send_create_signal('dashboard', ['PersonRelations'])

        # Adding model 'Animator'
        db.create_table(u'animator', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='NAME')),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, db_column='AGE', blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='GENDER')),
            ('csp_flag', self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='CSP_FLAG', blank=True)),
            ('camera_operator_flag', self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='CAMERA_OPERATOR_FLAG', blank=True)),
            ('facilitator_flag', self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='FACILITATOR_FLAG', blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='PHONE_NO', blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=500, db_column='ADDRESS', blank=True)),
            ('partner', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Partners'])),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'], db_column='home_village_id')),
            ('total_adoptions', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Animator'])

        # Adding unique constraint on 'Animator', fields ['name', 'gender', 'partner', 'village']
        db.create_unique(u'animator', ['NAME', 'GENDER', 'partner_id', 'home_village_id'])

        # Adding model 'Training'
        db.create_table(u'training', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('training_purpose', self.gf('django.db.models.fields.TextField')(db_column='TRAINING_PURPOSE', blank=True)),
            ('training_outcome', self.gf('django.db.models.fields.TextField')(db_column='TRAINING_OUTCOME', blank=True)),
            ('training_start_date', self.gf('django.db.models.fields.DateField')(db_column='TRAINING_START_DATE')),
            ('training_end_date', self.gf('django.db.models.fields.DateField')(db_column='TRAINING_END_DATE')),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('development_manager_present', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.DevelopmentManager'], null=True, db_column='dm_id', blank=True)),
            ('fieldofficer', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.FieldOfficer'], db_column='fieldofficer_id')),
        ))
        db.send_create_signal('dashboard', ['Training'])

        # Adding unique constraint on 'Training', fields ['training_start_date', 'training_end_date', 'village']
        db.create_unique(u'training', ['TRAINING_START_DATE', 'TRAINING_END_DATE', 'village_id'])

        # Adding model 'TrainingAnimatorsTrained'
        db.create_table(u'training_animators_trained', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('training', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Training'], db_column='training_id')),
            ('animator', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Animator'], db_column='animator_id')),
        ))
        db.send_create_signal('dashboard', ['TrainingAnimatorsTrained'])

        # Adding model 'AnimatorAssignedVillage'
        db.create_table(u'animator_assigned_village', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('animator', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Animator'])),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['AnimatorAssignedVillage'])

        # Adding model 'AnimatorSalaryPerMonth'
        db.create_table(u'animator_salary_per_month', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('animator', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Animator'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_column='DATE')),
            ('total_salary', self.gf('django.db.models.fields.FloatField')(null=True, db_column='TOTAL_SALARY', blank=True)),
            ('pay_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='PAY_DATE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['AnimatorSalaryPerMonth'])

        # Adding model 'Language'
        db.create_table(u'language', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('language_name', self.gf('django.db.models.fields.CharField')(unique='True', max_length=100)),
        ))
        db.send_create_signal('dashboard', ['Language'])

        # Adding model 'Video'
        db.create_table(u'video', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='TITLE')),
            ('video_type', self.gf('django.db.models.fields.IntegerField')(max_length=1, db_column='VIDEO_TYPE')),
            ('duration', self.gf('django.db.models.fields.TimeField')(null=True, db_column='DURATION', blank=True)),
            ('language', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Language'])),
            ('summary', self.gf('django.db.models.fields.TextField')(db_column='SUMMARY', blank=True)),
            ('picture_quality', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='PICTURE_QUALITY', blank=True)),
            ('audio_quality', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='AUDIO_QUALITY', blank=True)),
            ('editing_quality', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='EDITING_QUALITY', blank=True)),
            ('edit_start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='EDIT_START_DATE', blank=True)),
            ('edit_finish_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='EDIT_FINISH_DATE', blank=True)),
            ('thematic_quality', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='THEMATIC_QUALITY', blank=True)),
            ('video_production_start_date', self.gf('django.db.models.fields.DateField')(db_column='VIDEO_PRODUCTION_START_DATE')),
            ('video_production_end_date', self.gf('django.db.models.fields.DateField')(db_column='VIDEO_PRODUCTION_END_DATE')),
            ('storybase', self.gf('django.db.models.fields.IntegerField')(max_length=1, db_column='STORYBASE')),
            ('storyboard_filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, db_column='STORYBOARD_FILENAME', blank=True)),
            ('raw_filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, db_column='RAW_FILENAME', blank=True)),
            ('movie_maker_project_filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, db_column='MOVIE_MAKER_PROJECT_FILENAME', blank=True)),
            ('final_edited_filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, db_column='FINAL_EDITED_FILENAME', blank=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('facilitator', self.gf('dashboard.fields.BigForeignKey')(related_name='facilitator', to=orm['dashboard.Animator'])),
            ('cameraoperator', self.gf('dashboard.fields.BigForeignKey')(related_name='cameraoperator', to=orm['dashboard.Animator'])),
            ('reviewer', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Reviewer'], null=True, blank=True)),
            ('approval_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='APPROVAL_DATE', blank=True)),
            ('supplementary_video_produced', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Video'], null=True, blank=True)),
            ('video_suitable_for', self.gf('django.db.models.fields.IntegerField')(db_column='VIDEO_SUITABLE_FOR')),
            ('remarks', self.gf('django.db.models.fields.TextField')(db_column='REMARKS', blank=True)),
            ('related_practice', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Practices'], null=True, blank=True)),
            ('actors', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='ACTORS')),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('youtubeid', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='YOUTUBEID', blank=True)),
            ('viewers', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('dashboard', ['Video'])

        # Adding unique constraint on 'Video', fields ['title', 'video_production_start_date', 'video_production_end_date', 'village']
        db.create_unique(u'video', ['TITLE', 'VIDEO_PRODUCTION_START_DATE', 'VIDEO_PRODUCTION_END_DATE', 'village_id'])

        # Adding model 'PracticeSector'
        db.create_table(u'practice_sector', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dashboard', ['PracticeSector'])

        # Adding model 'PracticeSubSector'
        db.create_table(u'practice_subsector', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dashboard', ['PracticeSubSector'])

        # Adding model 'PracticeTopic'
        db.create_table(u'practice_topic', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dashboard', ['PracticeTopic'])

        # Adding model 'PracticeSubtopic'
        db.create_table(u'practice_subtopic', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dashboard', ['PracticeSubtopic'])

        # Adding model 'PracticeSubject'
        db.create_table(u'practice_subject', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dashboard', ['PracticeSubject'])

        # Adding model 'Practices'
        db.create_table(u'practices', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('practice_name', self.gf('django.db.models.fields.CharField')(max_length=200, unique='True', null=True, db_column='PRACTICE_NAME')),
            ('seasonality', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, db_column='SEASONALITY')),
            ('summary', self.gf('django.db.models.fields.TextField')(db_column='SUMMARY', blank=True)),
            ('practice_sector', self.gf('dashboard.fields.BigForeignKey')(default=1, to=orm['dashboard.PracticeSector'])),
            ('practice_subsector', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.PracticeSubSector'], null=True)),
            ('practice_topic', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.PracticeTopic'], null=True)),
            ('practice_subtopic', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.PracticeSubtopic'], null=True)),
            ('practice_subject', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.PracticeSubject'], null=True)),
        ))
        db.send_create_signal('dashboard', ['Practices'])

        # Adding unique constraint on 'Practices', fields ['practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject']
        db.create_unique(u'practices', ['practice_sector_id', 'practice_subsector_id', 'practice_topic_id', 'practice_subtopic_id', 'practice_subject_id'])

        # Adding model 'PersonShownInVideo'
        db.create_table(u'video_farmers_shown', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('video', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Video'], db_column='video_id')),
            ('person', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Person'], db_column='person_id')),
        ))
        db.send_create_signal('dashboard', ['PersonShownInVideo'])

        # Adding model 'Screening'
        db.create_table(u'screening', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(db_column='DATE')),
            ('start_time', self.gf('django.db.models.fields.TimeField')(db_column='START_TIME')),
            ('end_time', self.gf('django.db.models.fields.TimeField')(db_column='END_TIME')),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='LOCATION', blank=True)),
            ('target_person_attendance', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='TARGET_PERSON_ATTENDANCE', blank=True)),
            ('target_audience_interest', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='TARGET_AUDIENCE_INTEREST', blank=True)),
            ('target_adoptions', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='TARGET_ADOPTIONS', blank=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('fieldofficer', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.FieldOfficer'], null=True, blank=True)),
            ('animator', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Animator'])),
        ))
        db.send_create_signal('dashboard', ['Screening'])

        # Adding unique constraint on 'Screening', fields ['date', 'start_time', 'end_time', 'location', 'village']
        db.create_unique(u'screening', ['DATE', 'START_TIME', 'END_TIME', 'LOCATION', 'village_id'])

        # Adding model 'GroupsTargetedInScreening'
        db.create_table(u'screening_farmer_groups_targeted', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('screening', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Screening'], db_column='screening_id')),
            ('persongroups', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.PersonGroups'], db_column='persongroups_id')),
        ))
        db.send_create_signal('dashboard', ['GroupsTargetedInScreening'])

        # Adding model 'VideosScreenedInScreening'
        db.create_table(u'screening_videoes_screened', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('screening', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Screening'], db_column='screening_id')),
            ('video', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Video'], db_column='video_id')),
        ))
        db.send_create_signal('dashboard', ['VideosScreenedInScreening'])

        # Adding model 'PersonAdoptPractice'
        db.create_table(u'person_adopt_practice', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('person', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Person'])),
            ('video', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Video'])),
            ('prior_adoption_flag', self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='PRIOR_ADOPTION_FLAG', blank=True)),
            ('date_of_adoption', self.gf('django.db.models.fields.DateField')(db_column='DATE_OF_ADOPTION')),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='QUALITY', blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='QUANTITY', blank=True)),
            ('quantity_unit', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='QUANTITY_UNIT', blank=True)),
        ))
        db.send_create_signal('dashboard', ['PersonAdoptPractice'])

        # Adding unique constraint on 'PersonAdoptPractice', fields ['person', 'video', 'date_of_adoption']
        db.create_unique(u'person_adopt_practice', ['person_id', 'video_id', 'DATE_OF_ADOPTION'])

        # Adding model 'PersonMeetingAttendance'
        db.create_table(u'person_meeting_attendance', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('screening', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Screening'])),
            ('person', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Person'])),
            ('interested', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='INTERESTED', db_index=True)),
            ('expressed_question', self.gf('django.db.models.fields.CharField')(max_length=500, db_column='EXPRESSED_QUESTION', blank=True)),
            ('expressed_adoption_video', self.gf('dashboard.fields.BigForeignKey')(blank=True, related_name='expressed_adoption_video', null=True, db_column='EXPRESSED_ADOPTION_VIDEO', to=orm['dashboard.Video'])),
        ))
        db.send_create_signal('dashboard', ['PersonMeetingAttendance'])

        # Adding model 'Equipment'
        db.create_table(u'equipment_id', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('equipment_type', self.gf('django.db.models.fields.IntegerField')(db_column='EQUIPMENT_TYPE')),
            ('other_equipment', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, db_column='OTHER_EQUIPMENT', blank=True)),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='INVOICE_NO')),
            ('model_no', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='MODEL_NO', blank=True)),
            ('serial_no', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='SERIAL_NO', blank=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='COST', blank=True)),
            ('purpose', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='purpose', blank=True)),
            ('additional_accessories', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('is_reserve', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('procurement_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='PROCUREMENT_DATE', blank=True)),
            ('transfer_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('installation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('warranty_expiration_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='WARRANTY_EXPIRATION_DATE', blank=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'], null=True, blank=True)),
            ('equipmentholder', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.EquipmentHolder'], null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('dashboard', ['Equipment'])

        # Adding model 'UserPermission'
        db.create_table('dashboard_userpermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('region_operated', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Region'], null=True, blank=True)),
            ('district_operated', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.District'], null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['UserPermission'])

        # Adding model 'Target'
        db.create_table('dashboard_target', (
            ('id', self.gf('dashboard.fields.BigAutoField')(primary_key=True)),
            ('district', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.District'])),
            ('month_year', self.gf('django.db.models.fields.DateField')()),
            ('clusters_identification', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dg_concept_sharing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('csp_identification', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dissemination_set_deployment', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('village_operationalization', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_uploading', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_production', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('storyboard_preparation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_shooting', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_editing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_quality_checking', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('disseminations', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_attendance_per_dissemination', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exp_interest_per_dissemination', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('adoption_per_dissemination', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('crp_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('crp_refresher_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('csp_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('csp_refresher_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('editor_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('editor_refresher_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('villages_certification', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('what_went_well', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('what_not_went_well', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('challenges', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('support_requested', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Target'])

        # Adding unique constraint on 'Target', fields ['district', 'month_year']
        db.create_unique('dashboard_target', ['district_id', 'month_year'])

        # Adding model 'Rule'
        db.create_table('dashboard_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('error_msg', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('dashboard', ['Rule'])

        # Adding model 'Error'
        db.create_table('dashboard_error', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Rule'])),
            ('district', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.District'])),
            ('content_type1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type1', to=orm['contenttypes.ContentType'])),
            ('object_id1', self.gf('dashboard.fields.PositiveBigIntegerField')()),
            ('content_type2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type2', null=True, to=orm['contenttypes.ContentType'])),
            ('object_id2', self.gf('dashboard.fields.PositiveBigIntegerField')(null=True)),
            ('notanerror', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dashboard', ['Error'])

        # Adding unique constraint on 'Error', fields ['rule', 'content_type1', 'object_id1', 'content_type2', 'object_id2']
        db.create_unique('dashboard_error', ['rule_id', 'content_type1_id', 'object_id1', 'content_type2_id', 'object_id2'])

        # Adding model 'VillagePrecalculation'
        db.create_table(u'village_precalculation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('village', self.gf('dashboard.fields.BigForeignKey')(to=orm['dashboard.Village'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('total_adopted_attendees', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('total_active_attendees', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('total_adoption_by_active', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('dashboard', ['VillagePrecalculation'])

        # Adding unique constraint on 'VillagePrecalculation', fields ['village', 'date']
        db.create_unique(u'village_precalculation', ['village_id', 'date'])


    def backwards(self, orm):
        # Removing unique constraint on 'VillagePrecalculation', fields ['village', 'date']
        db.delete_unique(u'village_precalculation', ['village_id', 'date'])

        # Removing unique constraint on 'Error', fields ['rule', 'content_type1', 'object_id1', 'content_type2', 'object_id2']
        db.delete_unique('dashboard_error', ['rule_id', 'content_type1_id', 'object_id1', 'content_type2_id', 'object_id2'])

        # Removing unique constraint on 'Target', fields ['district', 'month_year']
        db.delete_unique('dashboard_target', ['district_id', 'month_year'])

        # Removing unique constraint on 'PersonAdoptPractice', fields ['person', 'video', 'date_of_adoption']
        db.delete_unique(u'person_adopt_practice', ['person_id', 'video_id', 'DATE_OF_ADOPTION'])

        # Removing unique constraint on 'Screening', fields ['date', 'start_time', 'end_time', 'location', 'village']
        db.delete_unique(u'screening', ['DATE', 'START_TIME', 'END_TIME', 'LOCATION', 'village_id'])

        # Removing unique constraint on 'Practices', fields ['practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject']
        db.delete_unique(u'practices', ['practice_sector_id', 'practice_subsector_id', 'practice_topic_id', 'practice_subtopic_id', 'practice_subject_id'])

        # Removing unique constraint on 'Video', fields ['title', 'video_production_start_date', 'video_production_end_date', 'village']
        db.delete_unique(u'video', ['TITLE', 'VIDEO_PRODUCTION_START_DATE', 'VIDEO_PRODUCTION_END_DATE', 'village_id'])

        # Removing unique constraint on 'Training', fields ['training_start_date', 'training_end_date', 'village']
        db.delete_unique(u'training', ['TRAINING_START_DATE', 'TRAINING_END_DATE', 'village_id'])

        # Removing unique constraint on 'Animator', fields ['name', 'gender', 'partner', 'village']
        db.delete_unique(u'animator', ['NAME', 'GENDER', 'partner_id', 'home_village_id'])

        # Removing unique constraint on 'Person', fields ['person_name', 'father_name', 'group', 'village']
        db.delete_unique(u'person', ['PERSON_NAME', 'FATHER_NAME', 'group_id', 'village_id'])

        # Removing unique constraint on 'PersonGroups', fields ['group_name', 'village']
        db.delete_unique(u'person_groups', ['GROUP_NAME', 'village_id'])

        # Removing unique constraint on 'Village', fields ['village_name', 'block']
        db.delete_unique(u'village', ['VILLAGE_NAME', 'block_id'])

        # Deleting model 'OfflineUser'
        db.delete_table('dashboard_offlineuser')

        # Deleting model 'RegionTest'
        db.delete_table(u'region_test')

        # Deleting model 'Region'
        db.delete_table(u'region')

        # Deleting model 'Country'
        db.delete_table(u'country')

        # Deleting model 'EquipmentHolder'
        db.delete_table(u'equipment_holder')

        # Deleting model 'Reviewer'
        db.delete_table(u'reviewer')

        # Deleting model 'DevelopmentManager'
        db.delete_table(u'development_manager')

        # Deleting model 'State'
        db.delete_table(u'state')

        # Deleting model 'Partners'
        db.delete_table(u'partner')

        # Deleting model 'FieldOfficer'
        db.delete_table(u'field_officer')

        # Deleting model 'District'
        db.delete_table(u'district')

        # Deleting model 'Block'
        db.delete_table(u'block')

        # Deleting model 'Village'
        db.delete_table(u'village')

        # Deleting model 'MonthlyCostPerVillage'
        db.delete_table(u'monthly_cost_per_village')

        # Deleting model 'PersonGroups'
        db.delete_table(u'person_groups')

        # Deleting model 'Person'
        db.delete_table(u'person')

        # Deleting model 'PersonRelations'
        db.delete_table(u'person_relations')

        # Deleting model 'Animator'
        db.delete_table(u'animator')

        # Deleting model 'Training'
        db.delete_table(u'training')

        # Deleting model 'TrainingAnimatorsTrained'
        db.delete_table(u'training_animators_trained')

        # Deleting model 'AnimatorAssignedVillage'
        db.delete_table(u'animator_assigned_village')

        # Deleting model 'AnimatorSalaryPerMonth'
        db.delete_table(u'animator_salary_per_month')

        # Deleting model 'Language'
        db.delete_table(u'language')

        # Deleting model 'Video'
        db.delete_table(u'video')

        # Deleting model 'PracticeSector'
        db.delete_table(u'practice_sector')

        # Deleting model 'PracticeSubSector'
        db.delete_table(u'practice_subsector')

        # Deleting model 'PracticeTopic'
        db.delete_table(u'practice_topic')

        # Deleting model 'PracticeSubtopic'
        db.delete_table(u'practice_subtopic')

        # Deleting model 'PracticeSubject'
        db.delete_table(u'practice_subject')

        # Deleting model 'Practices'
        db.delete_table(u'practices')

        # Deleting model 'PersonShownInVideo'
        db.delete_table(u'video_farmers_shown')

        # Deleting model 'Screening'
        db.delete_table(u'screening')

        # Deleting model 'GroupsTargetedInScreening'
        db.delete_table(u'screening_farmer_groups_targeted')

        # Deleting model 'VideosScreenedInScreening'
        db.delete_table(u'screening_videoes_screened')

        # Deleting model 'PersonAdoptPractice'
        db.delete_table(u'person_adopt_practice')

        # Deleting model 'PersonMeetingAttendance'
        db.delete_table(u'person_meeting_attendance')

        # Deleting model 'Equipment'
        db.delete_table(u'equipment_id')

        # Deleting model 'UserPermission'
        db.delete_table('dashboard_userpermission')

        # Deleting model 'Target'
        db.delete_table('dashboard_target')

        # Deleting model 'Rule'
        db.delete_table('dashboard_rule')

        # Deleting model 'Error'
        db.delete_table('dashboard_error')

        # Deleting model 'VillagePrecalculation'
        db.delete_table(u'village_precalculation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.animator': {
            'Meta': {'unique_together': "(('name', 'gender', 'partner', 'village'),)", 'object_name': 'Animator', 'db_table': "u'animator'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_villages'", 'to': "orm['dashboard.Village']", 'through': "orm['dashboard.AnimatorAssignedVillage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'camera_operator_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CAMERA_OPERATOR_FLAG'", 'blank': 'True'}),
            'csp_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CSP_FLAG'", 'blank': 'True'}),
            'facilitator_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'FACILITATOR_FLAG'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'total_adoptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'db_column': "'home_village_id'"})
        },
        'dashboard.animatorassignedvillage': {
            'Meta': {'object_name': 'AnimatorAssignedVillage', 'db_table': "u'animator_assigned_village'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.animatorsalarypermonth': {
            'Meta': {'object_name': 'AnimatorSalaryPerMonth', 'db_table': "u'animator_salary_per_month'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'pay_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PAY_DATE'", 'blank': 'True'}),
            'total_salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_SALARY'", 'blank': 'True'})
        },
        'dashboard.block': {
            'Meta': {'object_name': 'Block', 'db_table': "u'block'"},
            'block_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'BLOCK_NAME'"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'COUNTRY_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.developmentmanager': {
            'Meta': {'object_name': 'DevelopmentManager', 'db_table': "u'development_manager'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'}),
            'speciality': ('django.db.models.fields.TextField', [], {'db_column': "'SPECIALITY'", 'blank': 'True'}),
            'start_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DAY'", 'blank': 'True'})
        },
        'dashboard.district': {
            'Meta': {'object_name': 'District', 'db_table': "u'district'"},
            'district_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'DISTRICT_NAME'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']"}),
            'fieldofficer_startday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'FIELDOFFICER_STARTDAY'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.State']"})
        },
        'dashboard.equipment': {
            'Meta': {'object_name': 'Equipment', 'db_table': "u'equipment_id'"},
            'additional_accessories': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COST'", 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.IntegerField', [], {'db_column': "'EQUIPMENT_TYPE'"}),
            'equipmentholder': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.EquipmentHolder']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'installation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'INVOICE_NO'"}),
            'is_reserve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'MODEL_NO'", 'blank': 'True'}),
            'other_equipment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'db_column': "'OTHER_EQUIPMENT'", 'blank': 'True'}),
            'procurement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PROCUREMENT_DATE'", 'blank': 'True'}),
            'purpose': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'purpose'", 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'SERIAL_NO'", 'blank': 'True'}),
            'transfer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'null': 'True', 'blank': 'True'}),
            'warranty_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'WARRANTY_EXPIRATION_DATE'", 'blank': 'True'})
        },
        'dashboard.equipmentholder': {
            'Meta': {'object_name': 'EquipmentHolder', 'db_table': "u'equipment_holder'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {})
        },
        'dashboard.error': {
            'Meta': {'unique_together': "(('rule', 'content_type1', 'object_id1', 'content_type2', 'object_id2'),)", 'object_name': 'Error'},
            'content_type1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type1'", 'to': "orm['contenttypes.ContentType']"}),
            'content_type2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type2'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notanerror': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id1': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'object_id2': ('dashboard.fields.PositiveBigIntegerField', [], {'null': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Rule']"})
        },
        'dashboard.fieldofficer': {
            'Meta': {'object_name': 'FieldOfficer', 'db_table': "u'field_officer'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'})
        },
        'dashboard.groupstargetedinscreening': {
            'Meta': {'object_name': 'GroupsTargetedInScreening', 'db_table': "u'screening_farmer_groups_targeted'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'persongroups': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'db_column': "'persongroups_id'"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"})
        },
        'dashboard.language': {
            'Meta': {'object_name': 'Language', 'db_table': "u'language'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'})
        },
        'dashboard.monthlycostpervillage': {
            'Meta': {'object_name': 'MonthlyCostPerVillage', 'db_table': "u'monthly_cost_per_village'"},
            'community_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COMMUNITY_COST'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'digitalgreen_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'DIGITALGREEN_COST'", 'blank': 'True'}),
            'equipment_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'EQUIPMENT_COST'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'labor_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LABOR_COST'", 'blank': 'True'}),
            'miscellaneous_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'MISCELLANEOUS_COST'", 'blank': 'True'}),
            'partners_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'PARTNERS_COST'", 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_COST'", 'blank': 'True'}),
            'transportation_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TRANSPORTATION_COST'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.offlineuser': {
            'Meta': {'object_name': 'OfflineUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline_pk_id': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.partners': {
            'Meta': {'object_name': 'Partners', 'db_table': "u'partner'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'date_of_association': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'DATE_OF_ASSOCIATION'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PARTNER_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'})
        },
        'dashboard.person': {
            'Meta': {'unique_together': "(('person_name', 'father_name', 'group', 'village'),)", 'object_name': 'Person', 'db_table': "u'person'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'date_of_joining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'FATHER_NAME'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'group': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'image_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'land_holdings': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LAND_HOLDINGS'", 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PERSON_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rel'", 'to': "orm['dashboard.Person']", 'through': "orm['dashboard.PersonRelations']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personadoptpractice': {
            'Meta': {'unique_together': "(('person', 'video', 'date_of_adoption'),)", 'object_name': 'PersonAdoptPractice', 'db_table': "u'person_adopt_practice'"},
            'date_of_adoption': ('django.db.models.fields.DateField', [], {'db_column': "'DATE_OF_ADOPTION'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'prior_adoption_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'PRIOR_ADOPTION_FLAG'", 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'QUALITY'", 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'QUANTITY'", 'blank': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'QUANTITY_UNIT'", 'blank': 'True'}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']"})
        },
        'dashboard.persongroups': {
            'Meta': {'unique_together': "(('group_name', 'village'),)", 'object_name': 'PersonGroups', 'db_table': "u'person_groups'"},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'DAYS'", 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'GROUP_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'TIME_UPDATED'", 'blank': 'True'}),
            'timings': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'TIMINGS'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personmeetingattendance': {
            'Meta': {'object_name': 'PersonMeetingAttendance', 'db_table': "u'person_meeting_attendance'"},
            'expressed_adoption_video': ('dashboard.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_adoption_video'", 'null': 'True', 'db_column': "'EXPRESSED_ADOPTION_VIDEO'", 'to': "orm['dashboard.Video']"}),
            'expressed_question': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_QUESTION'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'interested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'INTERESTED'", 'db_index': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']"})
        },
        'dashboard.personrelations': {
            'Meta': {'object_name': 'PersonRelations', 'db_table': "u'person_relations'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'related_name': "'person'", 'to': "orm['dashboard.Person']"}),
            'relative': ('dashboard.fields.BigForeignKey', [], {'related_name': "'relative'", 'to': "orm['dashboard.Person']"}),
            'type_of_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'TYPE_OF_RELATIONSHIP'"})
        },
        'dashboard.personshowninvideo': {
            'Meta': {'object_name': 'PersonShownInVideo', 'db_table': "u'video_farmers_shown'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']", 'db_column': "'person_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.practices': {
            'Meta': {'unique_together': "(('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject'),)", 'object_name': 'Practices', 'db_table': "u'practices'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'practice_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': "'True'", 'null': 'True', 'db_column': "'PRACTICE_NAME'"}),
            'practice_sector': ('dashboard.fields.BigForeignKey', [], {'default': '1', 'to': "orm['dashboard.PracticeSector']"}),
            'practice_subject': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubject']", 'null': 'True'}),
            'practice_subsector': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubSector']", 'null': 'True'}),
            'practice_subtopic': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubtopic']", 'null': 'True'}),
            'practice_topic': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeTopic']", 'null': 'True'}),
            'seasonality': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "'SEASONALITY'"}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'})
        },
        'dashboard.practicesector': {
            'Meta': {'object_name': 'PracticeSector', 'db_table': "u'practice_sector'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicesubject': {
            'Meta': {'object_name': 'PracticeSubject', 'db_table': "u'practice_subject'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicesubsector': {
            'Meta': {'object_name': 'PracticeSubSector', 'db_table': "u'practice_subsector'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicesubtopic': {
            'Meta': {'object_name': 'PracticeSubtopic', 'db_table': "u'practice_subtopic'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.practicetopic': {
            'Meta': {'object_name': 'PracticeTopic', 'db_table': "u'practice_topic'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dashboard.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'region'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.regiontest': {
            'Meta': {'object_name': 'RegionTest', 'db_table': "u'region_test'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.reviewer': {
            'Meta': {'object_name': 'Reviewer', 'db_table': "u'reviewer'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {})
        },
        'dashboard.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_msg': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.screening': {
            'Meta': {'unique_together': "(('date', 'start_time', 'end_time', 'location', 'village'),)", 'object_name': 'Screening', 'db_table': "u'screening'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'db_column': "'END_TIME'"}),
            'farmer_groups_targeted': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.PersonGroups']", 'through': "orm['dashboard.GroupsTargetedInScreening']", 'symmetrical': 'False'}),
            'farmers_attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Person']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'LOCATION'", 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'db_column': "'START_TIME'"}),
            'target_adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_ADOPTIONS'", 'blank': 'True'}),
            'target_audience_interest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_AUDIENCE_INTEREST'", 'blank': 'True'}),
            'target_person_attendance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_PERSON_ATTENDANCE'", 'blank': 'True'}),
            'videoes_screened': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Video']", 'through': "orm['dashboard.VideosScreenedInScreening']", 'symmetrical': 'False'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.state': {
            'Meta': {'object_name': 'State', 'db_table': "u'state'"},
            'country': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Country']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'STATE_NAME'"})
        },
        'dashboard.target': {
            'Meta': {'unique_together': "(('district', 'month_year'),)", 'object_name': 'Target'},
            'adoption_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_attendance_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'challenges': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'clusters_identification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crp_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crp_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_identification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dg_concept_sharing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dissemination_set_deployment': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disseminations': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'editor_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'editor_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exp_interest_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'month_year': ('django.db.models.fields.DateField', [], {}),
            'storyboard_preparation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'support_requested': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video_editing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_production': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_quality_checking': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_shooting': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_uploading': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'village_operationalization': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'villages_certification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'what_not_went_well': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'what_went_well': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'dashboard.training': {
            'Meta': {'unique_together': "(('training_start_date', 'training_end_date', 'village'),)", 'object_name': 'Training', 'db_table': "u'training'"},
            'animators_trained': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Animator']", 'through': "orm['dashboard.TrainingAnimatorsTrained']", 'symmetrical': 'False'}),
            'development_manager_present': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.DevelopmentManager']", 'null': 'True', 'db_column': "'dm_id'", 'blank': 'True'}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'db_column': "'fieldofficer_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'training_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_END_DATE'"}),
            'training_outcome': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_OUTCOME'", 'blank': 'True'}),
            'training_purpose': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_PURPOSE'", 'blank': 'True'}),
            'training_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_START_DATE'"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.traininganimatorstrained': {
            'Meta': {'object_name': 'TrainingAnimatorsTrained', 'db_table': "u'training_animators_trained'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']", 'db_column': "'animator_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'training': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Training']", 'db_column': "'training_id'"})
        },
        'dashboard.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'district_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.video': {
            'Meta': {'unique_together': "(('title', 'video_production_start_date', 'video_production_end_date', 'village'),)", 'object_name': 'Video', 'db_table': "u'video'"},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'ACTORS'"}),
            'approval_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'APPROVAL_DATE'", 'blank': 'True'}),
            'audio_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'AUDIO_QUALITY'", 'blank': 'True'}),
            'cameraoperator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'cameraoperator'", 'to': "orm['dashboard.Animator']"}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'DURATION'", 'blank': 'True'}),
            'edit_finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_FINISH_DATE'", 'blank': 'True'}),
            'edit_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_START_DATE'", 'blank': 'True'}),
            'editing_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'EDITING_QUALITY'", 'blank': 'True'}),
            'facilitator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'facilitator'", 'to': "orm['dashboard.Animator']"}),
            'farmers_shown': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Person']", 'through': "orm['dashboard.PersonShownInVideo']", 'symmetrical': 'False'}),
            'final_edited_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'FINAL_EDITED_FILENAME'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Language']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'movie_maker_project_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'MOVIE_MAKER_PROJECT_FILENAME'", 'blank': 'True'}),
            'picture_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'PICTURE_QUALITY'", 'blank': 'True'}),
            'raw_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'RAW_FILENAME'", 'blank': 'True'}),
            'related_practice': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Practices']", 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'db_column': "'REMARKS'", 'blank': 'True'}),
            'reviewer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Reviewer']", 'null': 'True', 'blank': 'True'}),
            'storybase': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'STORYBASE'"}),
            'storyboard_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'STORYBOARD_FILENAME'", 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'supplementary_video_produced': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'null': 'True', 'blank': 'True'}),
            'thematic_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'THEMATIC_QUALITY'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'TITLE'"}),
            'video_production_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_END_DATE'"}),
            'video_production_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_START_DATE'"}),
            'video_suitable_for': ('django.db.models.fields.IntegerField', [], {'db_column': "'VIDEO_SUITABLE_FOR'"}),
            'video_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'VIDEO_TYPE'"}),
            'viewers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"}),
            'youtubeid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'YOUTUBEID'", 'blank': 'True'})
        },
        'dashboard.videosscreenedinscreening': {
            'Meta': {'object_name': 'VideosScreenedInScreening', 'db_table': "u'screening_videoes_screened'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village', 'db_table': "u'village'"},
            'block': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Block']"}),
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CONTROL'", 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'no_of_households': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'NO_OF_HOUSEHOLDS'", 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'POPULATION'", 'blank': 'True'}),
            'road_connectivity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'ROAD_CONNECTIVITY'", 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        },
        'dashboard.villageprecalculation': {
            'Meta': {'unique_together': "(('village', 'date'),)", 'object_name': 'VillagePrecalculation', 'db_table': "u'village_precalculation'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_active_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adopted_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adoption_by_active': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        }
    }

    complete_apps = ['dashboard']