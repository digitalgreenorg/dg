# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Screening', fields ['date', 'start_time', 'village', 'end_time', 'location']
        #db.db.execute('drop index myapp_mymodel_field1_667dc28f4f7b310_uniq on myapp_mymodel;')

        #db.delete_unique(u'screening', ['DATE', 'START_TIME', 'village_id', 'END_TIME', 'LOCATION'])

        # Removing unique constraint on 'VillagePrecalculation', fields ['village', 'date']
        db.delete_unique(u'village_precalculation', ['village_id', 'date'])

        # Removing unique constraint on 'Training', fields ['training_start_date', 'training_end_date', 'village']
        #db.delete_unique(u'training', ['TRAINING_START_DATE', 'TRAINING_END_DATE', 'village_id'])

        # Removing unique constraint on 'Target', fields ['district', 'month_year']
        #db.delete_unique('dashboard_target', ['district_id', 'month_year'])

        # Deleting model 'Target'
        db.delete_table('dashboard_target')

        # Deleting model 'Equipment'
        db.delete_table(u'equipment_id')

        # Deleting model 'RegionTest'
        db.delete_table(u'region_test')

        # Deleting model 'TrainingAnimatorsTrained'
        db.delete_table(u'training_animators_trained')

        # Deleting model 'MonthlyCostPerVillage'
        db.delete_table(u'monthly_cost_per_village')

        # Deleting model 'Training'
        db.delete_table(u'training')

        # Removing M2M table for field animators_trained on 'Training'
        #db.delete_table('training_animators_trained')

        # Deleting model 'AnimatorSalaryPerMonth'
        db.delete_table(u'animator_salary_per_month')

        # Deleting model 'VillagePrecalculation'
        db.delete_table(u'village_precalculation')

        # Deleting model 'PersonRelations'
        db.delete_table(u'person_relations')

        # Deleting model 'EquipmentHolder'
        db.delete_table(u'equipment_holder')

        # Deleting field 'Video.edit_finish_date'
        db.delete_column(u'video', 'EDIT_FINISH_DATE')

        # Deleting field 'Video.movie_maker_project_filename'
        db.delete_column(u'video', 'MOVIE_MAKER_PROJECT_FILENAME')

        # Deleting field 'Video.last_modified'
        db.delete_column(u'video', 'last_modified')

        # Deleting field 'Video.edit_start_date'
        db.delete_column(u'video', 'EDIT_START_DATE')

        # Deleting field 'Video.final_edited_filename'
        db.delete_column(u'video', 'FINAL_EDITED_FILENAME')

        # Deleting field 'Video.editing_quality'
        db.delete_column(u'video', 'EDITING_QUALITY')

        # Deleting field 'Video.raw_filename'
        db.delete_column(u'video', 'RAW_FILENAME')

        # Deleting field 'Video.audio_quality'
        db.delete_column(u'video', 'AUDIO_QUALITY')

        # Deleting field 'Video.remarks'
        db.delete_column(u'video', 'REMARKS')

        # Deleting field 'Video.supplementary_video_produced'
        db.delete_column(u'video', 'supplementary_video_produced_id')

        # Deleting field 'Video.storybase'
        db.delete_column(u'video', 'STORYBASE')

        # Deleting field 'Video.storyboard_filename'
        db.delete_column(u'video', 'STORYBOARD_FILENAME')

        # Deleting field 'Video.picture_quality'
        db.delete_column(u'video', 'PICTURE_QUALITY')

        # Deleting field 'Video.thematic_quality'
        db.delete_column(u'video', 'THEMATIC_QUALITY')

        # Deleting field 'Animator.camera_operator_flag'
        db.delete_column(u'animator', 'CAMERA_OPERATOR_FLAG')

        # Deleting field 'Animator.csp_flag'
        db.delete_column(u'animator', 'CSP_FLAG')

        # Deleting field 'Animator.facilitator_flag'
        db.delete_column(u'animator', 'FACILITATOR_FLAG')

        # Deleting field 'Animator.address'
        db.delete_column(u'animator', 'ADDRESS')

        # Deleting field 'Village.no_of_households'
        db.delete_column(u'village', 'NO_OF_HOUSEHOLDS')

        # Deleting field 'Village.road_connectivity'
        db.delete_column(u'village', 'ROAD_CONNECTIVITY')

        # Deleting field 'Village.population'
        db.delete_column(u'village', 'POPULATION')

        # Deleting field 'Screening.target_adoptions'
        db.delete_column(u'screening', 'TARGET_ADOPTIONS')

        # Deleting field 'Screening.target_person_attendance'
        db.delete_column(u'screening', 'TARGET_PERSON_ATTENDANCE')

        # Deleting field 'Screening.location'
        db.delete_column(u'screening', 'LOCATION')

        # Deleting field 'Screening.target_audience_interest'
        db.delete_column(u'screening', 'TARGET_AUDIENCE_INTEREST')

        # Adding unique constraint on 'Screening', fields ['date', 'start_time', 'animator', 'end_time', 'village']
        db.create_unique(u'screening', ['DATE', 'START_TIME', 'animator_id', 'END_TIME', 'village_id'])

        # Deleting field 'PersonAdoptPractice.time_updated'
        db.delete_column(u'person_adopt_practice', 'time_updated')

        # Deleting field 'Practices.seasonality'
        db.delete_column(u'practices', 'SEASONALITY')


    def backwards(self, orm):
        # Removing unique constraint on 'Screening', fields ['date', 'start_time', 'animator', 'end_time', 'village']
        #db.delete_unique(u'screening', ['DATE', 'START_TIME', 'animator_id', 'END_TIME', 'village_id'])

        # Adding model 'Target'
        db.create_table('dashboard_target', (
            ('what_went_well', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('video_uploading', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('storyboard_preparation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('crp_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('csp_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('challenges', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('support_requested', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('video_editing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dg_concept_sharing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_created', null=True, to=orm['auth.User'], blank=True)),
            ('avg_attendance_per_dissemination', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('video_quality_checking', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('clusters_identification', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('village_operationalization', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('what_not_went_well', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('district', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.District'])),
            ('editor_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_shooting', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('csp_refresher_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dissemination_set_deployment', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('adoption_per_dissemination', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('villages_certification', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('disseminations', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_production', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('crp_refresher_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('month_year', self.gf('django.db.models.fields.DateField')()),
            ('csp_identification', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('editor_refresher_training', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exp_interest_per_dissemination', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Target'])

        # Adding unique constraint on 'Target', fields ['district', 'month_year']
        #db.create_unique('dashboard_target', ['district_id', 'month_year'])

        # Adding model 'Equipment'
        db.create_table(u'equipment_id', (
            ('serial_no', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='SERIAL_NO', blank=True)),
            ('additional_accessories', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='COST', blank=True)),
            ('village', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Village'], null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipment_created', null=True, to=orm['auth.User'], blank=True)),
            ('other_equipment', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, db_column='OTHER_EQUIPMENT', blank=True)),
            ('procurement_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='PROCUREMENT_DATE', blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipment_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('equipmentholder', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.EquipmentHolder'], null=True, blank=True)),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('installation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('model_no', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='MODEL_NO', blank=True)),
            ('purpose', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='purpose', blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=300, db_column='INVOICE_NO')),
            ('equipment_type', self.gf('django.db.models.fields.IntegerField')(db_column='EQUIPMENT_TYPE')),
            ('warranty_expiration_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='WARRANTY_EXPIRATION_DATE', blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('is_reserve', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transfer_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['Equipment'])

        # Adding model 'RegionTest'
        db.create_table(u'region_test', (
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('region_name', self.gf('django.db.models.fields.CharField')(max_length=100, unique='True', db_column='REGION_NAME')),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regiontest_created', null=True, to=orm['auth.User'], blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='regiontest_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='id')),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='START_DATE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['RegionTest'])

        # Adding model 'TrainingAnimatorsTrained'
        db.create_table(u'training_animators_trained', (
            ('training', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Training'], db_column='training_id')),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('animator', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Animator'], db_column='animator_id')),
        ))
        db.send_create_signal('dashboard', ['TrainingAnimatorsTrained'])

        # Adding model 'MonthlyCostPerVillage'
        db.create_table(u'monthly_cost_per_village', (
            ('digitalgreen_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='DIGITALGREEN_COST', blank=True)),
            ('labor_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='LABOR_COST', blank=True)),
            ('partners_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='PARTNERS_COST', blank=True)),
            ('total_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='TOTAL_COST', blank=True)),
            ('community_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='COMMUNITY_COST', blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='monthlycostpervillage_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('miscellaneous_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='MISCELLANEOUS_COST', blank=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('transportation_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='TRANSPORTATION_COST', blank=True)),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='monthlycostpervillage_created', null=True, to=orm['auth.User'], blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('equipment_cost', self.gf('django.db.models.fields.FloatField')(null=True, db_column='EQUIPMENT_COST', blank=True)),
            ('village', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Village'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_column='DATE')),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
        ))
        db.send_create_signal('dashboard', ['MonthlyCostPerVillage'])

        # Adding model 'Training'
        db.create_table(u'training', (
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('village', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Village'])),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='training_created', null=True, to=orm['auth.User'], blank=True)),
            ('training_start_date', self.gf('django.db.models.fields.DateField')(db_column='TRAINING_START_DATE')),
            ('training_end_date', self.gf('django.db.models.fields.DateField')(db_column='TRAINING_END_DATE')),
            ('development_manager_present', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.DevelopmentManager'], null=True, db_column='dm_id', blank=True)),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('training_outcome', self.gf('django.db.models.fields.TextField')(db_column='TRAINING_OUTCOME', blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='training_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('fieldofficer', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.FieldOfficer'], db_column='fieldofficer_id')),
            ('training_purpose', self.gf('django.db.models.fields.TextField')(db_column='TRAINING_PURPOSE', blank=True)),
        ))
        db.send_create_signal('dashboard', ['Training'])

        # Adding M2M table for field animators_trained on 'Training'
#        db.create_table(u'training_animators_trained', (
#            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
#            ('training', models.ForeignKey(orm['dashboard.training'], null=False)),
#            ('animator', models.ForeignKey(orm['dashboard.animator'], null=False))
#        ))
        #db.create_unique(u'training_animators_trained', ['training_id', 'animator_id'])

        # Adding unique constraint on 'Training', fields ['training_start_date', 'training_end_date', 'village']
        #db.create_unique(u'training', ['TRAINING_START_DATE', 'TRAINING_END_DATE', 'village_id'])

        # Adding model 'AnimatorSalaryPerMonth'
        db.create_table(u'animator_salary_per_month', (
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='animatorsalarypermonth_created', null=True, to=orm['auth.User'], blank=True)),
            ('pay_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='PAY_DATE', blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(db_column='DATE')),
            ('total_salary', self.gf('django.db.models.fields.FloatField')(null=True, db_column='TOTAL_SALARY', blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='animatorsalarypermonth_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('animator', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Animator'])),
        ))
        db.send_create_signal('dashboard', ['AnimatorSalaryPerMonth'])

        # Adding model 'VillagePrecalculation'
        db.create_table(u'village_precalculation', (
            ('total_adopted_attendees', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('total_active_attendees', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('village', self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Village'])),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='villageprecalculation_created', null=True, to=orm['auth.User'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('total_adoption_by_active', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='villageprecalculation_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('dashboard', ['VillagePrecalculation'])

        # Adding unique constraint on 'VillagePrecalculation', fields ['village', 'date']
        db.create_unique(u'village_precalculation', ['village_id', 'date'])

        # Adding model 'PersonRelations'
        db.create_table(u'person_relations', (
            ('relative', self.gf('dashboard.fields.related.BigForeignKey')(related_name='relative', to=orm['dashboard.Person'])),
            ('person', self.gf('dashboard.fields.related.BigForeignKey')(related_name='person', to=orm['dashboard.Person'])),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('type_of_relationship', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='TYPE_OF_RELATIONSHIP')),
        ))
        db.send_create_signal('dashboard', ['PersonRelations'])

        # Adding model 'EquipmentHolder'
        db.create_table(u'equipment_holder', (
            ('time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('user_created', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipmentholder_created', null=True, to=orm['auth.User'], blank=True)),
            ('user_modified', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipmentholder_related_modified', null=True, to=orm['auth.User'], blank=True)),
            ('id', self.gf('dashboard.fields.fields.BigAutoField')(primary_key=True)),
            ('object_id', self.gf('dashboard.fields.fields.PositiveBigIntegerField')()),
        ))
        db.send_create_signal('dashboard', ['EquipmentHolder'])

        # Adding field 'Video.edit_finish_date'
        db.add_column(u'video', 'edit_finish_date',
                      self.gf('django.db.models.fields.DateField')(null=True, db_column='EDIT_FINISH_DATE', blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Video.movie_maker_project_filename'
        raise RuntimeError("Cannot reverse this migration. 'Video.movie_maker_project_filename' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Video.last_modified'
        raise RuntimeError("Cannot reverse this migration. 'Video.last_modified' and its values cannot be restored.")
        # Adding field 'Video.edit_start_date'
        db.add_column(u'video', 'edit_start_date',
                      self.gf('django.db.models.fields.DateField')(null=True, db_column='EDIT_START_DATE', blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Video.final_edited_filename'
        raise RuntimeError("Cannot reverse this migration. 'Video.final_edited_filename' and its values cannot be restored.")
        # Adding field 'Video.editing_quality'
        db.add_column(u'video', 'editing_quality',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, db_column='EDITING_QUALITY', blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Video.raw_filename'
        raise RuntimeError("Cannot reverse this migration. 'Video.raw_filename' and its values cannot be restored.")
        # Adding field 'Video.audio_quality'
        db.add_column(u'video', 'audio_quality',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, db_column='AUDIO_QUALITY', blank=True),
                      keep_default=False)

        # Adding field 'Video.remarks'
        db.add_column(u'video', 'remarks',
                      self.gf('django.db.models.fields.TextField')(default='', db_column='REMARKS', blank=True),
                      keep_default=False)

        # Adding field 'Video.supplementary_video_produced'
        db.add_column(u'video', 'supplementary_video_produced',
                      self.gf('dashboard.fields.related.BigForeignKey')(to=orm['dashboard.Video'], null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Video.storybase'
        raise RuntimeError("Cannot reverse this migration. 'Video.storybase' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Video.storyboard_filename'
        raise RuntimeError("Cannot reverse this migration. 'Video.storyboard_filename' and its values cannot be restored.")
        # Adding field 'Video.picture_quality'
        db.add_column(u'video', 'picture_quality',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, db_column='PICTURE_QUALITY', blank=True),
                      keep_default=False)

        # Adding field 'Video.thematic_quality'
        db.add_column(u'video', 'thematic_quality',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, db_column='THEMATIC_QUALITY', blank=True),
                      keep_default=False)

        # Adding field 'Animator.camera_operator_flag'
        db.add_column(u'animator', 'camera_operator_flag',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='CAMERA_OPERATOR_FLAG', blank=True),
                      keep_default=False)

        # Adding field 'Animator.csp_flag'
        db.add_column(u'animator', 'csp_flag',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='CSP_FLAG', blank=True),
                      keep_default=False)

        # Adding field 'Animator.facilitator_flag'
        db.add_column(u'animator', 'facilitator_flag',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, db_column='FACILITATOR_FLAG', blank=True),
                      keep_default=False)

        # Adding field 'Animator.address'
        db.add_column(u'animator', 'address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, db_column='ADDRESS', blank=True),
                      keep_default=False)

        # Adding field 'Village.no_of_households'
        db.add_column(u'village', 'no_of_households',
                      self.gf('django.db.models.fields.IntegerField')(null=True, db_column='NO_OF_HOUSEHOLDS', blank=True),
                      keep_default=False)

        # Adding field 'Village.road_connectivity'
        db.add_column(u'village', 'road_connectivity',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, db_column='ROAD_CONNECTIVITY', blank=True),
                      keep_default=False)

        # Adding field 'Village.population'
        db.add_column(u'village', 'population',
                      self.gf('django.db.models.fields.IntegerField')(null=True, db_column='POPULATION', blank=True),
                      keep_default=False)

        # Adding field 'Screening.target_adoptions'
        db.add_column(u'screening', 'target_adoptions',
                      self.gf('django.db.models.fields.IntegerField')(null=True, db_column='TARGET_ADOPTIONS', blank=True),
                      keep_default=False)

        # Adding field 'Screening.target_person_attendance'
        db.add_column(u'screening', 'target_person_attendance',
                      self.gf('django.db.models.fields.IntegerField')(null=True, db_column='TARGET_PERSON_ATTENDANCE', blank=True),
                      keep_default=False)

        # Adding field 'Screening.location'
        db.add_column(u'screening', 'location',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, db_column='LOCATION', blank=True),
                      keep_default=False)

        # Adding field 'Screening.target_audience_interest'
        db.add_column(u'screening', 'target_audience_interest',
                      self.gf('django.db.models.fields.IntegerField')(null=True, db_column='TARGET_AUDIENCE_INTEREST', blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Screening', fields ['date', 'start_time', 'village', 'end_time', 'location']
        #db.create_unique(u'screening', ['DATE', 'START_TIME', 'village_id', 'END_TIME', 'LOCATION'])

        # Adding field 'PersonAdoptPractice.time_updated'
        db.add_column(u'person_adopt_practice', 'time_updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Practices.seasonality'
        db.add_column(u'practices', 'seasonality',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, db_column='SEASONALITY'),
                      keep_default=False)


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
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_animators'", 'to': "orm['dashboard.Village']", 'through': "orm['dashboard.AnimatorAssignedVillage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'partner': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'total_adoptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animator_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animator_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'db_column': "'home_village_id'"})
        },
        'dashboard.animatorassignedvillage': {
            'Meta': {'object_name': 'AnimatorAssignedVillage', 'db_table': "u'animator_assigned_village'"},
            'animator': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorassignedvillage_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorassignedvillage_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.block': {
            'Meta': {'object_name': 'Block', 'db_table': "u'block'"},
            'block_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'BLOCK_NAME'"}),
            'district': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'block_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'block_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'COUNTRY_NAME'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'country_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'country_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.developmentmanager': {
            'Meta': {'object_name': 'DevelopmentManager', 'db_table': "u'development_manager'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'region': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'}),
            'speciality': ('django.db.models.fields.TextField', [], {'db_column': "'SPECIALITY'", 'blank': 'True'}),
            'start_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DAY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'developmentmanager_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'developmentmanager_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.district': {
            'Meta': {'object_name': 'District', 'db_table': "u'district'"},
            'district_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'DISTRICT_NAME'"}),
            'fieldofficer': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']"}),
            'fieldofficer_startday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'FIELDOFFICER_STARTDAY'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.State']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'district_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'district_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.error': {
            'Meta': {'unique_together': "(('rule', 'content_type1', 'object_id1', 'content_type2', 'object_id2'),)", 'object_name': 'Error'},
            'content_type1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type1'", 'to': "orm['contenttypes.ContentType']"}),
            'content_type2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type2'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'district': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notanerror': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id1': ('dashboard.fields.fields.PositiveBigIntegerField', [], {}),
            'object_id2': ('dashboard.fields.fields.PositiveBigIntegerField', [], {'null': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Rule']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'error_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'error_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.fieldofficer': {
            'Meta': {'object_name': 'FieldOfficer', 'db_table': "u'field_officer'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fieldofficer_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fieldofficer_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.groupstargetedinscreening': {
            'Meta': {'object_name': 'GroupsTargetedInScreening', 'db_table': "u'screening_farmer_groups_targeted'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'persongroups': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'db_column': "'persongroups_id'"}),
            'screening': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"})
        },
        'dashboard.language': {
            'Meta': {'object_name': 'Language', 'db_table': "u'language'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.offlineuser': {
            'Meta': {'object_name': 'OfflineUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline_pk_id': ('dashboard.fields.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'offlineuser_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'offlineuser_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.partners': {
            'Meta': {'object_name': 'Partners', 'db_table': "u'partners'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'date_of_association': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'DATE_OF_ASSOCIATION'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PARTNER_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.person': {
            'Meta': {'unique_together': "(('person_name', 'father_name', 'group', 'village'),)", 'object_name': 'Person', 'db_table': "u'person'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'date_of_joining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'FATHER_NAME'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'group': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'image_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'land_holdings': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LAND_HOLDINGS'", 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PERSON_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'person_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'person_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personadoptpractice': {
            'Meta': {'unique_together': "(('person', 'video', 'date_of_adoption'),)", 'object_name': 'PersonAdoptPractice', 'db_table': "u'person_adopt_practice'"},
            'date_of_adoption': ('django.db.models.fields.DateField', [], {'db_column': "'DATE_OF_ADOPTION'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'prior_adoption_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'PRIOR_ADOPTION_FLAG'", 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'QUALITY'", 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'QUANTITY'", 'blank': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'QUANTITY_UNIT'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personadoptpractice_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personadoptpractice_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Video']"})
        },
        'dashboard.persongroups': {
            'Meta': {'unique_together': "(('group_name', 'village'),)", 'object_name': 'PersonGroups', 'db_table': "u'person_groups'"},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'DAYS'", 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'GROUP_NAME'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'TIME_UPDATED'", 'blank': 'True'}),
            'timings': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'TIMINGS'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'persongroups_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'persongroups_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personmeetingattendance': {
            'Meta': {'object_name': 'PersonMeetingAttendance', 'db_table': "u'person_meeting_attendance'"},
            'expressed_adoption_video': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'null': 'True', 'db_column': "'EXPRESSED_ADOPTION_VIDEO'", 'blank': 'True'}),
            'expressed_question': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_QUESTION'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'interested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'INTERESTED'", 'db_index': 'True'}),
            'person': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'screening': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Screening']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personmeetingattendance_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personmeetingattendance_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.personshowninvideo': {
            'Meta': {'object_name': 'PersonShownInVideo', 'db_table': "u'video_farmers_shown'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Person']", 'db_column': "'person_id'"}),
            'video': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.practices': {
            'Meta': {'unique_together': "(('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject'),)", 'object_name': 'Practices', 'db_table': "u'practices'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'practice_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': "'True'", 'null': 'True', 'db_column': "'PRACTICE_NAME'"}),
            'practice_sector': ('dashboard.fields.related.BigForeignKey', [], {'default': '1', 'to': "orm['dashboard.PracticeSector']"}),
            'practice_subject': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubject']", 'null': 'True'}),
            'practice_subsector': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubSector']", 'null': 'True'}),
            'practice_subtopic': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubtopic']", 'null': 'True'}),
            'practice_topic': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.PracticeTopic']", 'null': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practices_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practices_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesector': {
            'Meta': {'object_name': 'PracticeSector', 'db_table': "u'practice_sector'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesector_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesector_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubject': {
            'Meta': {'object_name': 'PracticeSubject', 'db_table': "u'practice_subject'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubject_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubject_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubsector': {
            'Meta': {'object_name': 'PracticeSubSector', 'db_table': "u'practice_subsector'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubsector_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubsector_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubtopic': {
            'Meta': {'object_name': 'PracticeSubtopic', 'db_table': "u'practice_subtopic'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubtopic_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubtopic_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicetopic': {
            'Meta': {'object_name': 'PracticeTopic', 'db_table': "u'practice_topic'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicetopic_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicetopic_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'region'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.reviewer': {
            'Meta': {'object_name': 'Reviewer', 'db_table': "u'reviewer'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_msg': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rule_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rule_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.screening': {
            'Meta': {'unique_together': "(('date', 'start_time', 'end_time', 'village', 'animator'),)", 'object_name': 'Screening', 'db_table': "u'screening'"},
            'animator': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'db_column': "'END_TIME'"}),
            'farmer_groups_targeted': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.PersonGroups']", 'symmetrical': 'False'}),
            'farmers_attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Person']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'fieldofficer': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'db_column': "'START_TIME'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'screening_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'screening_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'videoes_screened': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.Video']", 'symmetrical': 'False'}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.state': {
            'Meta': {'object_name': 'State', 'db_table': "u'state'"},
            'country': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Country']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'STATE_NAME'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'district_operated': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.District']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_operated': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Region']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userpermission_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userpermission_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.video': {
            'Meta': {'unique_together': "(('title', 'video_production_start_date', 'video_production_end_date', 'village'),)", 'object_name': 'Video', 'db_table': "u'video'"},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'ACTORS'"}),
            'approval_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'APPROVAL_DATE'", 'blank': 'True'}),
            'cameraoperator': ('dashboard.fields.related.BigForeignKey', [], {'related_name': "'videos_shot'", 'to': "orm['dashboard.Animator']"}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'DURATION'", 'blank': 'True'}),
            'facilitator': ('dashboard.fields.related.BigForeignKey', [], {'related_name': "'videos_facilitated'", 'to': "orm['dashboard.Animator']"}),
            'farmers_shown': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.Person']", 'symmetrical': 'False'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Language']"}),
            'related_practice': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Practices']", 'null': 'True', 'blank': 'True'}),
            'reviewer': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Reviewer']", 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'TITLE'"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video_production_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_END_DATE'"}),
            'video_production_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_START_DATE'"}),
            'video_suitable_for': ('django.db.models.fields.IntegerField', [], {'db_column': "'VIDEO_SUITABLE_FOR'"}),
            'video_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'VIDEO_TYPE'"}),
            'viewers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"}),
            'youtubeid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'YOUTUBEID'", 'blank': 'True'})
        },
        'dashboard.videosscreenedinscreening': {
            'Meta': {'object_name': 'VideosScreenedInScreening', 'db_table': "u'screening_videoes_screened'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'screening': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"}),
            'video': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village', 'db_table': "u'village'"},
            'block': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Block']"}),
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CONTROL'", 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        }
    }

    complete_apps = ['dashboard']