# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Person.user_created'
        db.add_column(u'PERSON', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='person_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Person.time_created'
        db.add_column(u'PERSON', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Person.user_modified'
        db.add_column(u'PERSON', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='person_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Person.time_modified'
        db.add_column(u'PERSON', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PersonShownInVideo.user_created'
        db.add_column(u'VIDEO_farmers_shown', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personshowninvideo_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonShownInVideo.time_created'
        db.add_column(u'VIDEO_farmers_shown', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PersonShownInVideo.user_modified'
        db.add_column(u'VIDEO_farmers_shown', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personshowninvideo_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonShownInVideo.time_modified'
        db.add_column(u'VIDEO_farmers_shown', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Target.user_created'
        db.add_column('dashboard_target', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='target_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Target.time_created'
        db.add_column('dashboard_target', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Target.user_modified'
        db.add_column('dashboard_target', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='target_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Target.time_modified'
        db.add_column('dashboard_target', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'DevelopmentManager.user_created'
        db.add_column(u'DEVELOPMENT_MANAGER', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='developmentmanager_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'DevelopmentManager.time_created'
        db.add_column(u'DEVELOPMENT_MANAGER', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'DevelopmentManager.user_modified'
        db.add_column(u'DEVELOPMENT_MANAGER', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='developmentmanager_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'DevelopmentManager.time_modified'
        db.add_column(u'DEVELOPMENT_MANAGER', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Equipment.user_created'
        db.add_column(u'EQUIPMENT_ID', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipment_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Equipment.time_created'
        db.add_column(u'EQUIPMENT_ID', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Equipment.user_modified'
        db.add_column(u'EQUIPMENT_ID', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipment_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Equipment.time_modified'
        db.add_column(u'EQUIPMENT_ID', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'State.user_created'
        db.add_column(u'STATE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='state_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'State.time_created'
        db.add_column(u'STATE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'State.user_modified'
        db.add_column(u'STATE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='state_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'State.time_modified'
        db.add_column(u'STATE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PersonAdoptPractice.user_created'
        db.add_column(u'PERSON_ADOPT_PRACTICE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personadoptpractice_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonAdoptPractice.time_created'
        db.add_column(u'PERSON_ADOPT_PRACTICE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PersonAdoptPractice.user_modified'
        db.add_column(u'PERSON_ADOPT_PRACTICE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personadoptpractice_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonAdoptPractice.time_modified'
        db.add_column(u'PERSON_ADOPT_PRACTICE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Video.user_created'
        db.add_column(u'VIDEO', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='video_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Video.time_created'
        db.add_column(u'VIDEO', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Video.user_modified'
        db.add_column(u'VIDEO', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='video_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Video.time_modified'
        db.add_column(u'VIDEO', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Animator.user_created'
        db.add_column(u'ANIMATOR', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animator_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Animator.time_created'
        db.add_column(u'ANIMATOR', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Animator.user_modified'
        db.add_column(u'ANIMATOR', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animator_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Animator.time_modified'
        db.add_column(u'ANIMATOR', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'RegionTest.user_created'
        db.add_column(u'REGION_TEST', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='regiontest_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'RegionTest.time_created'
        db.add_column(u'REGION_TEST', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'RegionTest.user_modified'
        db.add_column(u'REGION_TEST', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='regiontest_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'RegionTest.time_modified'
        db.add_column(u'REGION_TEST', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'TrainingAnimatorsTrained.user_created'
        db.add_column(u'TRAINING_animators_trained', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='traininganimatorstrained_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'TrainingAnimatorsTrained.time_created'
        db.add_column(u'TRAINING_animators_trained', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'TrainingAnimatorsTrained.user_modified'
        db.add_column(u'TRAINING_animators_trained', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='traininganimatorstrained_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'TrainingAnimatorsTrained.time_modified'
        db.add_column(u'TRAINING_animators_trained', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'GroupsTargetedInScreening.user_created'
        db.add_column(u'SCREENING_farmer_groups_targeted', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='groupstargetedinscreening_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'GroupsTargetedInScreening.time_created'
        db.add_column(u'SCREENING_farmer_groups_targeted', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'GroupsTargetedInScreening.user_modified'
        db.add_column(u'SCREENING_farmer_groups_targeted', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='groupstargetedinscreening_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'GroupsTargetedInScreening.time_modified'
        db.add_column(u'SCREENING_farmer_groups_targeted', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Country.user_created'
        db.add_column(u'COUNTRY', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='country_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Country.time_created'
        db.add_column(u'COUNTRY', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Country.user_modified'
        db.add_column(u'COUNTRY', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='country_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Country.time_modified'
        db.add_column(u'COUNTRY', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Rule.user_created'
        db.add_column('dashboard_rule', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rule_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Rule.time_created'
        db.add_column('dashboard_rule', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Rule.user_modified'
        db.add_column('dashboard_rule', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rule_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Rule.time_modified'
        db.add_column('dashboard_rule', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Partners.user_created'
        db.add_column(u'PARTNERS', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='partners_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Partners.time_created'
        db.add_column(u'PARTNERS', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Partners.user_modified'
        db.add_column(u'PARTNERS', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='partners_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Partners.time_modified'
        db.add_column(u'PARTNERS', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Training.user_created'
        db.add_column(u'TRAINING', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='training_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Training.time_created'
        db.add_column(u'TRAINING', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Training.user_modified'
        db.add_column(u'TRAINING', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='training_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Training.time_modified'
        db.add_column(u'TRAINING', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PracticeSector.user_created'
        db.add_column(u'practice_sector', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesector_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PracticeSector.time_created'
        db.add_column(u'practice_sector', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PracticeSector.user_modified'
        db.add_column(u'practice_sector', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesector_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PracticeSector.time_modified'
        db.add_column(u'practice_sector', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'UserPermission.user_created'
        db.add_column('dashboard_userpermission', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userpermission_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'UserPermission.time_created'
        db.add_column('dashboard_userpermission', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'UserPermission.user_modified'
        db.add_column('dashboard_userpermission', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userpermission_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'UserPermission.time_modified'
        db.add_column('dashboard_userpermission', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Language.user_created'
        db.add_column(u'LANGUAGE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='language_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Language.time_created'
        db.add_column(u'LANGUAGE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Language.user_modified'
        db.add_column(u'LANGUAGE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='language_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Language.time_modified'
        db.add_column(u'LANGUAGE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Error.user_created'
        db.add_column('dashboard_error', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='error_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Error.time_created'
        db.add_column('dashboard_error', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Error.user_modified'
        db.add_column('dashboard_error', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='error_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Error.time_modified'
        db.add_column('dashboard_error', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Reviewer.user_created'
        db.add_column(u'REVIEWER', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reviewer_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Reviewer.time_created'
        db.add_column(u'REVIEWER', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Reviewer.user_modified'
        db.add_column(u'REVIEWER', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reviewer_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Reviewer.time_modified'
        db.add_column(u'REVIEWER', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.user_created'
        db.add_column(u'ANIMATOR_SALARY_PER_MONTH', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorsalarypermonth_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.time_created'
        db.add_column(u'ANIMATOR_SALARY_PER_MONTH', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.user_modified'
        db.add_column(u'ANIMATOR_SALARY_PER_MONTH', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorsalarypermonth_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.time_modified'
        db.add_column(u'ANIMATOR_SALARY_PER_MONTH', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'VillagePrecalculation.user_created'
        db.add_column(u'village_precalculation', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='villageprecalculation_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'VillagePrecalculation.time_created'
        db.add_column(u'village_precalculation', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'VillagePrecalculation.user_modified'
        db.add_column(u'village_precalculation', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='villageprecalculation_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'VillagePrecalculation.time_modified'
        db.add_column(u'village_precalculation', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PracticeSubSector.user_created'
        db.add_column(u'practice_subsector', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubsector_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PracticeSubSector.time_created'
        db.add_column(u'practice_subsector', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PracticeSubSector.user_modified'
        db.add_column(u'practice_subsector', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubsector_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PracticeSubSector.time_modified'
        db.add_column(u'practice_subsector', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PersonRelations.user_created'
        db.add_column(u'PERSON_RELATIONS', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personrelations_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonRelations.time_created'
        db.add_column(u'PERSON_RELATIONS', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PersonRelations.user_modified'
        db.add_column(u'PERSON_RELATIONS', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personrelations_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonRelations.time_modified'
        db.add_column(u'PERSON_RELATIONS', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'FieldOfficer.user_created'
        db.add_column(u'FIELD_OFFICER', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fieldofficer_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'FieldOfficer.time_created'
        db.add_column(u'FIELD_OFFICER', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'FieldOfficer.user_modified'
        db.add_column(u'FIELD_OFFICER', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fieldofficer_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'FieldOfficer.time_modified'
        db.add_column(u'FIELD_OFFICER', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'VideosScreenedInScreening.user_created'
        db.add_column(u'SCREENING_videoes_screened', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='videosscreenedinscreening_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'VideosScreenedInScreening.time_created'
        db.add_column(u'SCREENING_videoes_screened', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'VideosScreenedInScreening.user_modified'
        db.add_column(u'SCREENING_videoes_screened', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='videosscreenedinscreening_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'VideosScreenedInScreening.time_modified'
        db.add_column(u'SCREENING_videoes_screened', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Region.user_created'
        db.add_column(u'REGION', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='region_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Region.time_created'
        db.add_column(u'REGION', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Region.user_modified'
        db.add_column(u'REGION', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='region_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Region.time_modified'
        db.add_column(u'REGION', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Block.user_created'
        db.add_column(u'BLOCK', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='block_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Block.time_created'
        db.add_column(u'BLOCK', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Block.user_modified'
        db.add_column(u'BLOCK', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='block_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Block.time_modified'
        db.add_column(u'BLOCK', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Village.user_created'
        db.add_column(u'VILLAGE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='village_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Village.time_created'
        db.add_column(u'VILLAGE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Village.user_modified'
        db.add_column(u'VILLAGE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='village_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Village.time_modified'
        db.add_column(u'VILLAGE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Screening.user_created'
        db.add_column(u'SCREENING', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='screening_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Screening.time_created'
        db.add_column(u'SCREENING', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Screening.user_modified'
        db.add_column(u'SCREENING', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='screening_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Screening.time_modified'
        db.add_column(u'SCREENING', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PracticeSubject.user_created'
        db.add_column(u'practice_subject', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubject_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PracticeSubject.time_created'
        db.add_column(u'practice_subject', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PracticeSubject.user_modified'
        db.add_column(u'practice_subject', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubject_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PracticeSubject.time_modified'
        db.add_column(u'practice_subject', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PersonMeetingAttendance.user_created'
        db.add_column(u'PERSON_MEETING_ATTENDANCE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personmeetingattendance_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonMeetingAttendance.time_created'
        db.add_column(u'PERSON_MEETING_ATTENDANCE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PersonMeetingAttendance.user_modified'
        db.add_column(u'PERSON_MEETING_ATTENDANCE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personmeetingattendance_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonMeetingAttendance.time_modified'
        db.add_column(u'PERSON_MEETING_ATTENDANCE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'EquipmentHolder.user_created'
        db.add_column(u'EQUIPMENT_HOLDER', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipmentholder_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'EquipmentHolder.time_created'
        db.add_column(u'EQUIPMENT_HOLDER', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'EquipmentHolder.user_modified'
        db.add_column(u'EQUIPMENT_HOLDER', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipmentholder_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'EquipmentHolder.time_modified'
        db.add_column(u'EQUIPMENT_HOLDER', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'AnimatorAssignedVillage.user_created'
        db.add_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorassignedvillage_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'AnimatorAssignedVillage.time_created'
        db.add_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'AnimatorAssignedVillage.user_modified'
        db.add_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorassignedvillage_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'AnimatorAssignedVillage.time_modified'
        db.add_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'MonthlyCostPerVillage.user_created'
        db.add_column(u'MONTHLY_COST_PER_VILLAGE', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='monthlycostpervillage_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'MonthlyCostPerVillage.time_created'
        db.add_column(u'MONTHLY_COST_PER_VILLAGE', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'MonthlyCostPerVillage.user_modified'
        db.add_column(u'MONTHLY_COST_PER_VILLAGE', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='monthlycostpervillage_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'MonthlyCostPerVillage.time_modified'
        db.add_column(u'MONTHLY_COST_PER_VILLAGE', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'Practices.user_created'
        db.add_column(u'PRACTICES', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practices_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Practices.time_created'
        db.add_column(u'PRACTICES', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'Practices.user_modified'
        db.add_column(u'PRACTICES', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practices_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Practices.time_modified'
        db.add_column(u'PRACTICES', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'District.user_created'
        db.add_column(u'DISTRICT', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='district_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'District.time_created'
        db.add_column(u'DISTRICT', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'District.user_modified'
        db.add_column(u'DISTRICT', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='district_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'District.time_modified'
        db.add_column(u'DISTRICT', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)

        # Adding field 'PersonGroups.user_created'
        db.add_column(u'PERSON_GROUPS', 'user_created', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='persongroups_related_created', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonGroups.time_created'
        db.add_column(u'PERSON_GROUPS', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='TIME_CREATED', blank=True), keep_default=False)

        # Adding field 'PersonGroups.user_modified'
        db.add_column(u'PERSON_GROUPS', 'user_modified', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='persongroups_related_modified', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'PersonGroups.time_modified'
        db.add_column(u'PERSON_GROUPS', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, db_column='TIME_MODIFIED', blank=True), keep_default=False)


    def backwards(self, orm):

        # Deleting field 'Person.user_created'
        db.delete_column(u'PERSON', 'user_created_id')

        # Deleting field 'Person.time_created'
        db.delete_column(u'PERSON', 'TIME_CREATED')

        # Deleting field 'Person.user_modified'
        db.delete_column(u'PERSON', 'user_modified_id')

        # Deleting field 'Person.time_modified'
        db.delete_column(u'PERSON', 'TIME_MODIFIED')

        # Deleting field 'PersonShownInVideo.user_created'
        db.delete_column(u'VIDEO_farmers_shown', 'user_created_id')

        # Deleting field 'PersonShownInVideo.time_created'
        db.delete_column(u'VIDEO_farmers_shown', 'TIME_CREATED')

        # Deleting field 'PersonShownInVideo.user_modified'
        db.delete_column(u'VIDEO_farmers_shown', 'user_modified_id')

        # Deleting field 'PersonShownInVideo.time_modified'
        db.delete_column(u'VIDEO_farmers_shown', 'TIME_MODIFIED')

        # Deleting field 'Target.user_created'
        db.delete_column('dashboard_target', 'user_created_id')

        # Deleting field 'Target.time_created'
        db.delete_column('dashboard_target', 'TIME_CREATED')

        # Deleting field 'Target.user_modified'
        db.delete_column('dashboard_target', 'user_modified_id')

        # Deleting field 'Target.time_modified'
        db.delete_column('dashboard_target', 'TIME_MODIFIED')

        # Deleting field 'DevelopmentManager.user_created'
        db.delete_column(u'DEVELOPMENT_MANAGER', 'user_created_id')

        # Deleting field 'DevelopmentManager.time_created'
        db.delete_column(u'DEVELOPMENT_MANAGER', 'TIME_CREATED')

        # Deleting field 'DevelopmentManager.user_modified'
        db.delete_column(u'DEVELOPMENT_MANAGER', 'user_modified_id')

        # Deleting field 'DevelopmentManager.time_modified'
        db.delete_column(u'DEVELOPMENT_MANAGER', 'TIME_MODIFIED')

        # Deleting field 'Equipment.user_created'
        db.delete_column(u'EQUIPMENT_ID', 'user_created_id')

        # Deleting field 'Equipment.time_created'
        db.delete_column(u'EQUIPMENT_ID', 'TIME_CREATED')

        # Deleting field 'Equipment.user_modified'
        db.delete_column(u'EQUIPMENT_ID', 'user_modified_id')

        # Deleting field 'Equipment.time_modified'
        db.delete_column(u'EQUIPMENT_ID', 'TIME_MODIFIED')

        # Deleting field 'State.user_created'
        db.delete_column(u'STATE', 'user_created_id')

        # Deleting field 'State.time_created'
        db.delete_column(u'STATE', 'TIME_CREATED')

        # Deleting field 'State.user_modified'
        db.delete_column(u'STATE', 'user_modified_id')

        # Deleting field 'State.time_modified'
        db.delete_column(u'STATE', 'TIME_MODIFIED')

        # Deleting field 'PersonAdoptPractice.user_created'
        db.delete_column(u'PERSON_ADOPT_PRACTICE', 'user_created_id')

        # Deleting field 'PersonAdoptPractice.time_created'
        db.delete_column(u'PERSON_ADOPT_PRACTICE', 'TIME_CREATED')

        # Deleting field 'PersonAdoptPractice.user_modified'
        db.delete_column(u'PERSON_ADOPT_PRACTICE', 'user_modified_id')

        # Deleting field 'PersonAdoptPractice.time_modified'
        db.delete_column(u'PERSON_ADOPT_PRACTICE', 'TIME_MODIFIED')

        # Deleting field 'Video.user_created'
        db.delete_column(u'VIDEO', 'user_created_id')

        # Deleting field 'Video.time_created'
        db.delete_column(u'VIDEO', 'TIME_CREATED')

        # Deleting field 'Video.user_modified'
        db.delete_column(u'VIDEO', 'user_modified_id')

        # Deleting field 'Video.time_modified'
        db.delete_column(u'VIDEO', 'TIME_MODIFIED')

        # Deleting field 'Animator.user_created'
        db.delete_column(u'ANIMATOR', 'user_created_id')

        # Deleting field 'Animator.time_created'
        db.delete_column(u'ANIMATOR', 'TIME_CREATED')

        # Deleting field 'Animator.user_modified'
        db.delete_column(u'ANIMATOR', 'user_modified_id')

        # Deleting field 'Animator.time_modified'
        db.delete_column(u'ANIMATOR', 'TIME_MODIFIED')

        # Deleting field 'RegionTest.user_created'
        db.delete_column(u'REGION_TEST', 'user_created_id')

        # Deleting field 'RegionTest.time_created'
        db.delete_column(u'REGION_TEST', 'TIME_CREATED')

        # Deleting field 'RegionTest.user_modified'
        db.delete_column(u'REGION_TEST', 'user_modified_id')

        # Deleting field 'RegionTest.time_modified'
        db.delete_column(u'REGION_TEST', 'TIME_MODIFIED')

        # Deleting field 'TrainingAnimatorsTrained.user_created'
        db.delete_column(u'TRAINING_animators_trained', 'user_created_id')

        # Deleting field 'TrainingAnimatorsTrained.time_created'
        db.delete_column(u'TRAINING_animators_trained', 'TIME_CREATED')

        # Deleting field 'TrainingAnimatorsTrained.user_modified'
        db.delete_column(u'TRAINING_animators_trained', 'user_modified_id')

        # Deleting field 'TrainingAnimatorsTrained.time_modified'
        db.delete_column(u'TRAINING_animators_trained', 'TIME_MODIFIED')

        # Deleting field 'GroupsTargetedInScreening.user_created'
        db.delete_column(u'SCREENING_farmer_groups_targeted', 'user_created_id')

        # Deleting field 'GroupsTargetedInScreening.time_created'
        db.delete_column(u'SCREENING_farmer_groups_targeted', 'TIME_CREATED')

        # Deleting field 'GroupsTargetedInScreening.user_modified'
        db.delete_column(u'SCREENING_farmer_groups_targeted', 'user_modified_id')

        # Deleting field 'GroupsTargetedInScreening.time_modified'
        db.delete_column(u'SCREENING_farmer_groups_targeted', 'TIME_MODIFIED')

        # Deleting field 'Country.user_created'
        db.delete_column(u'COUNTRY', 'user_created_id')

        # Deleting field 'Country.time_created'
        db.delete_column(u'COUNTRY', 'TIME_CREATED')

        # Deleting field 'Country.user_modified'
        db.delete_column(u'COUNTRY', 'user_modified_id')

        # Deleting field 'Country.time_modified'
        db.delete_column(u'COUNTRY', 'TIME_MODIFIED')

        # Deleting field 'Rule.user_created'
        db.delete_column('dashboard_rule', 'user_created_id')

        # Deleting field 'Rule.time_created'
        db.delete_column('dashboard_rule', 'TIME_CREATED')

        # Deleting field 'Rule.user_modified'
        db.delete_column('dashboard_rule', 'user_modified_id')

        # Deleting field 'Rule.time_modified'
        db.delete_column('dashboard_rule', 'TIME_MODIFIED')

        # Deleting field 'Partners.user_created'
        db.delete_column(u'PARTNERS', 'user_created_id')

        # Deleting field 'Partners.time_created'
        db.delete_column(u'PARTNERS', 'TIME_CREATED')

        # Deleting field 'Partners.user_modified'
        db.delete_column(u'PARTNERS', 'user_modified_id')

        # Deleting field 'Partners.time_modified'
        db.delete_column(u'PARTNERS', 'TIME_MODIFIED')

        # Deleting field 'Training.user_created'
        db.delete_column(u'TRAINING', 'user_created_id')

        # Deleting field 'Training.time_created'
        db.delete_column(u'TRAINING', 'TIME_CREATED')

        # Deleting field 'Training.user_modified'
        db.delete_column(u'TRAINING', 'user_modified_id')

        # Deleting field 'Training.time_modified'
        db.delete_column(u'TRAINING', 'TIME_MODIFIED')

        # Deleting field 'PracticeSector.user_created'
        db.delete_column(u'practice_sector', 'user_created_id')

        # Deleting field 'PracticeSector.time_created'
        db.delete_column(u'practice_sector', 'TIME_CREATED')

        # Deleting field 'PracticeSector.user_modified'
        db.delete_column(u'practice_sector', 'user_modified_id')

        # Deleting field 'PracticeSector.time_modified'
        db.delete_column(u'practice_sector', 'TIME_MODIFIED')

        # Deleting field 'UserPermission.user_created'
        db.delete_column('dashboard_userpermission', 'user_created_id')

        # Deleting field 'UserPermission.time_created'
        db.delete_column('dashboard_userpermission', 'TIME_CREATED')

        # Deleting field 'UserPermission.user_modified'
        db.delete_column('dashboard_userpermission', 'user_modified_id')

        # Deleting field 'UserPermission.time_modified'
        db.delete_column('dashboard_userpermission', 'TIME_MODIFIED')

        # Deleting field 'Language.user_created'
        db.delete_column(u'LANGUAGE', 'user_created_id')

        # Deleting field 'Language.time_created'
        db.delete_column(u'LANGUAGE', 'TIME_CREATED')

        # Deleting field 'Language.user_modified'
        db.delete_column(u'LANGUAGE', 'user_modified_id')

        # Deleting field 'Language.time_modified'
        db.delete_column(u'LANGUAGE', 'TIME_MODIFIED')

        # Deleting field 'Error.user_created'
        db.delete_column('dashboard_error', 'user_created_id')

        # Deleting field 'Error.time_created'
        db.delete_column('dashboard_error', 'TIME_CREATED')

        # Deleting field 'Error.user_modified'
        db.delete_column('dashboard_error', 'user_modified_id')

        # Deleting field 'Error.time_modified'
        db.delete_column('dashboard_error', 'TIME_MODIFIED')

        # Deleting field 'Reviewer.user_created'
        db.delete_column(u'REVIEWER', 'user_created_id')

        # Deleting field 'Reviewer.time_created'
        db.delete_column(u'REVIEWER', 'TIME_CREATED')

        # Deleting field 'Reviewer.user_modified'
        db.delete_column(u'REVIEWER', 'user_modified_id')

        # Deleting field 'Reviewer.time_modified'
        db.delete_column(u'REVIEWER', 'TIME_MODIFIED')

        # Deleting field 'AnimatorSalaryPerMonth.user_created'
        db.delete_column(u'ANIMATOR_SALARY_PER_MONTH', 'user_created_id')

        # Deleting field 'AnimatorSalaryPerMonth.time_created'
        db.delete_column(u'ANIMATOR_SALARY_PER_MONTH', 'TIME_CREATED')

        # Deleting field 'AnimatorSalaryPerMonth.user_modified'
        db.delete_column(u'ANIMATOR_SALARY_PER_MONTH', 'user_modified_id')

        # Deleting field 'AnimatorSalaryPerMonth.time_modified'
        db.delete_column(u'ANIMATOR_SALARY_PER_MONTH', 'TIME_MODIFIED')

        # Deleting field 'VillagePrecalculation.user_created'
        db.delete_column(u'village_precalculation', 'user_created_id')

        # Deleting field 'VillagePrecalculation.time_created'
        db.delete_column(u'village_precalculation', 'TIME_CREATED')

        # Deleting field 'VillagePrecalculation.user_modified'
        db.delete_column(u'village_precalculation', 'user_modified_id')

        # Deleting field 'VillagePrecalculation.time_modified'
        db.delete_column(u'village_precalculation', 'TIME_MODIFIED')

        # Deleting field 'PracticeSubSector.user_created'
        db.delete_column(u'practice_subsector', 'user_created_id')

        # Deleting field 'PracticeSubSector.time_created'
        db.delete_column(u'practice_subsector', 'TIME_CREATED')

        # Deleting field 'PracticeSubSector.user_modified'
        db.delete_column(u'practice_subsector', 'user_modified_id')

        # Deleting field 'PracticeSubSector.time_modified'
        db.delete_column(u'practice_subsector', 'TIME_MODIFIED')

        # Deleting field 'PersonRelations.user_created'
        db.delete_column(u'PERSON_RELATIONS', 'user_created_id')

        # Deleting field 'PersonRelations.time_created'
        db.delete_column(u'PERSON_RELATIONS', 'TIME_CREATED')

        # Deleting field 'PersonRelations.user_modified'
        db.delete_column(u'PERSON_RELATIONS', 'user_modified_id')

        # Deleting field 'PersonRelations.time_modified'
        db.delete_column(u'PERSON_RELATIONS', 'TIME_MODIFIED')

        # Deleting field 'FieldOfficer.user_created'
        db.delete_column(u'FIELD_OFFICER', 'user_created_id')

        # Deleting field 'FieldOfficer.time_created'
        db.delete_column(u'FIELD_OFFICER', 'TIME_CREATED')

        # Deleting field 'FieldOfficer.user_modified'
        db.delete_column(u'FIELD_OFFICER', 'user_modified_id')

        # Deleting field 'FieldOfficer.time_modified'
        db.delete_column(u'FIELD_OFFICER', 'TIME_MODIFIED')

        # Deleting field 'VideosScreenedInScreening.user_created'
        db.delete_column(u'SCREENING_videoes_screened', 'user_created_id')

        # Deleting field 'VideosScreenedInScreening.time_created'
        db.delete_column(u'SCREENING_videoes_screened', 'TIME_CREATED')

        # Deleting field 'VideosScreenedInScreening.user_modified'
        db.delete_column(u'SCREENING_videoes_screened', 'user_modified_id')

        # Deleting field 'VideosScreenedInScreening.time_modified'
        db.delete_column(u'SCREENING_videoes_screened', 'TIME_MODIFIED')

        # Deleting field 'Region.user_created'
        db.delete_column(u'REGION', 'user_created_id')

        # Deleting field 'Region.time_created'
        db.delete_column(u'REGION', 'TIME_CREATED')

        # Deleting field 'Region.user_modified'
        db.delete_column(u'REGION', 'user_modified_id')

        # Deleting field 'Region.time_modified'
        db.delete_column(u'REGION', 'TIME_MODIFIED')

        # Deleting field 'Block.user_created'
        db.delete_column(u'BLOCK', 'user_created_id')

        # Deleting field 'Block.time_created'
        db.delete_column(u'BLOCK', 'TIME_CREATED')

        # Deleting field 'Block.user_modified'
        db.delete_column(u'BLOCK', 'user_modified_id')

        # Deleting field 'Block.time_modified'
        db.delete_column(u'BLOCK', 'TIME_MODIFIED')

        # Deleting field 'Village.user_created'
        db.delete_column(u'VILLAGE', 'user_created_id')

        # Deleting field 'Village.time_created'
        db.delete_column(u'VILLAGE', 'TIME_CREATED')

        # Deleting field 'Village.user_modified'
        db.delete_column(u'VILLAGE', 'user_modified_id')

        # Deleting field 'Village.time_modified'
        db.delete_column(u'VILLAGE', 'TIME_MODIFIED')

        # Deleting field 'Screening.user_created'
        db.delete_column(u'SCREENING', 'user_created_id')

        # Deleting field 'Screening.time_created'
        db.delete_column(u'SCREENING', 'TIME_CREATED')

        # Deleting field 'Screening.user_modified'
        db.delete_column(u'SCREENING', 'user_modified_id')

        # Deleting field 'Screening.time_modified'
        db.delete_column(u'SCREENING', 'TIME_MODIFIED')

        # Deleting field 'PracticeSubject.user_created'
        db.delete_column(u'practice_subject', 'user_created_id')

        # Deleting field 'PracticeSubject.time_created'
        db.delete_column(u'practice_subject', 'TIME_CREATED')

        # Deleting field 'PracticeSubject.user_modified'
        db.delete_column(u'practice_subject', 'user_modified_id')

        # Deleting field 'PracticeSubject.time_modified'
        db.delete_column(u'practice_subject', 'TIME_MODIFIED')

        # Deleting field 'PersonMeetingAttendance.user_created'
        db.delete_column(u'PERSON_MEETING_ATTENDANCE', 'user_created_id')

        # Deleting field 'PersonMeetingAttendance.time_created'
        db.delete_column(u'PERSON_MEETING_ATTENDANCE', 'TIME_CREATED')

        # Deleting field 'PersonMeetingAttendance.user_modified'
        db.delete_column(u'PERSON_MEETING_ATTENDANCE', 'user_modified_id')

        # Deleting field 'PersonMeetingAttendance.time_modified'
        db.delete_column(u'PERSON_MEETING_ATTENDANCE', 'TIME_MODIFIED')

        # Deleting field 'EquipmentHolder.user_created'
        db.delete_column(u'EQUIPMENT_HOLDER', 'user_created_id')

        # Deleting field 'EquipmentHolder.time_created'
        db.delete_column(u'EQUIPMENT_HOLDER', 'TIME_CREATED')

        # Deleting field 'EquipmentHolder.user_modified'
        db.delete_column(u'EQUIPMENT_HOLDER', 'user_modified_id')

        # Deleting field 'EquipmentHolder.time_modified'
        db.delete_column(u'EQUIPMENT_HOLDER', 'TIME_MODIFIED')

        # Deleting field 'AnimatorAssignedVillage.user_created'
        db.delete_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'user_created_id')

        # Deleting field 'AnimatorAssignedVillage.time_created'
        db.delete_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'TIME_CREATED')

        # Deleting field 'AnimatorAssignedVillage.user_modified'
        db.delete_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'user_modified_id')

        # Deleting field 'AnimatorAssignedVillage.time_modified'
        db.delete_column(u'ANIMATOR_ASSIGNED_VILLAGE', 'TIME_MODIFIED')

        # Deleting field 'MonthlyCostPerVillage.user_created'
        db.delete_column(u'MONTHLY_COST_PER_VILLAGE', 'user_created_id')

        # Deleting field 'MonthlyCostPerVillage.time_created'
        db.delete_column(u'MONTHLY_COST_PER_VILLAGE', 'TIME_CREATED')

        # Deleting field 'MonthlyCostPerVillage.user_modified'
        db.delete_column(u'MONTHLY_COST_PER_VILLAGE', 'user_modified_id')

        # Deleting field 'MonthlyCostPerVillage.time_modified'
        db.delete_column(u'MONTHLY_COST_PER_VILLAGE', 'TIME_MODIFIED')

        # Deleting field 'Practices.user_created'
        db.delete_column(u'PRACTICES', 'user_created_id')

        # Deleting field 'Practices.time_created'
        db.delete_column(u'PRACTICES', 'TIME_CREATED')

        # Deleting field 'Practices.user_modified'
        db.delete_column(u'PRACTICES', 'user_modified_id')

        # Deleting field 'Practices.time_modified'
        db.delete_column(u'PRACTICES', 'TIME_MODIFIED')

        # Deleting field 'District.user_created'
        db.delete_column(u'DISTRICT', 'user_created_id')

        # Deleting field 'District.time_created'
        db.delete_column(u'DISTRICT', 'TIME_CREATED')

        # Deleting field 'District.user_modified'
        db.delete_column(u'DISTRICT', 'user_modified_id')

        # Deleting field 'District.time_modified'
        db.delete_column(u'DISTRICT', 'TIME_MODIFIED')

        # Deleting field 'PersonGroups.user_created'
        db.delete_column(u'PERSON_GROUPS', 'user_created_id')

        # Deleting field 'PersonGroups.time_created'
        db.delete_column(u'PERSON_GROUPS', 'TIME_CREATED')

        # Deleting field 'PersonGroups.user_modified'
        db.delete_column(u'PERSON_GROUPS', 'user_modified_id')

        # Deleting field 'PersonGroups.time_modified'
        db.delete_column(u'PERSON_GROUPS', 'TIME_MODIFIED')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 14, 25, 7, 726000)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 14, 25, 7, 726000)'}),
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
            'Meta': {'unique_together': "(('name', 'gender', 'partner', 'village'),)", 'object_name': 'Animator', 'db_table': "u'ANIMATOR'"},
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'total_adoptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animator_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animator_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'db_column': "'home_village_id'"})
        },
        'dashboard.animatorassignedvillage': {
            'Meta': {'object_name': 'AnimatorAssignedVillage', 'db_table': "u'ANIMATOR_ASSIGNED_VILLAGE'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorassignedvillage_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorassignedvillage_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.animatorsalarypermonth': {
            'Meta': {'object_name': 'AnimatorSalaryPerMonth', 'db_table': "u'ANIMATOR_SALARY_PER_MONTH'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'pay_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PAY_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'total_salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_SALARY'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorsalarypermonth_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorsalarypermonth_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.block': {
            'Meta': {'object_name': 'Block', 'db_table': "u'BLOCK'"},
            'block_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'BLOCK_NAME'"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'block_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'block_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'COUNTRY'"},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'COUNTRY_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'country_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'country_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.developmentmanager': {
            'Meta': {'object_name': 'DevelopmentManager', 'db_table': "u'DEVELOPMENT_MANAGER'"},
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
            'start_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DAY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'developmentmanager_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'developmentmanager_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.district': {
            'Meta': {'object_name': 'District', 'db_table': "u'DISTRICT'"},
            'district_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'DISTRICT_NAME'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']"}),
            'fieldofficer_startday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'FIELDOFFICER_STARTDAY'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.State']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'district_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'district_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.equipment': {
            'Meta': {'object_name': 'Equipment', 'db_table': "u'EQUIPMENT_ID'"},
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'transfer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipment_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipment_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'null': 'True', 'blank': 'True'}),
            'warranty_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'WARRANTY_EXPIRATION_DATE'", 'blank': 'True'})
        },
        'dashboard.equipmentholder': {
            'Meta': {'object_name': 'EquipmentHolder', 'db_table': "u'EQUIPMENT_HOLDER'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipmentholder_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipmentholder_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
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
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Rule']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'error_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'error_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.fieldofficer': {
            'Meta': {'object_name': 'FieldOfficer', 'db_table': "u'FIELD_OFFICER'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fieldofficer_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fieldofficer_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.groupstargetedinscreening': {
            'Meta': {'object_name': 'GroupsTargetedInScreening', 'db_table': "u'SCREENING_farmer_groups_targeted'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'persongroups': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'db_column': "'persongroups_id'"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'groupstargetedinscreening_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'groupstargetedinscreening_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.language': {
            'Meta': {'object_name': 'Language', 'db_table': "u'LANGUAGE'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.monthlycostpervillage': {
            'Meta': {'object_name': 'MonthlyCostPerVillage', 'db_table': "u'MONTHLY_COST_PER_VILLAGE'"},
            'community_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COMMUNITY_COST'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'digitalgreen_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'DIGITALGREEN_COST'", 'blank': 'True'}),
            'equipment_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'EQUIPMENT_COST'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'labor_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LABOR_COST'", 'blank': 'True'}),
            'miscellaneous_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'MISCELLANEOUS_COST'", 'blank': 'True'}),
            'partners_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'PARTNERS_COST'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_COST'", 'blank': 'True'}),
            'transportation_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TRANSPORTATION_COST'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'monthlycostpervillage_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'monthlycostpervillage_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.offlineuser': {
            'Meta': {'object_name': 'OfflineUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline_pk_id': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'offlineuser_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'offlineuser_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.partners': {
            'Meta': {'object_name': 'Partners', 'db_table': "u'PARTNERS'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'date_of_association': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'DATE_OF_ASSOCIATION'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PARTNER_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.person': {
            'Meta': {'unique_together': "(('person_name', 'father_name', 'group', 'village'),)", 'object_name': 'Person', 'db_table': "u'PERSON'"},
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'person_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'person_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personadoptpractice': {
            'Meta': {'unique_together': "(('person', 'video', 'date_of_adoption'),)", 'object_name': 'PersonAdoptPractice', 'db_table': "u'PERSON_ADOPT_PRACTICE'"},
            'date_of_adoption': ('django.db.models.fields.DateField', [], {'db_column': "'DATE_OF_ADOPTION'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'prior_adoption_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'PRIOR_ADOPTION_FLAG'", 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'QUALITY'", 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'QUANTITY'", 'blank': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'QUANTITY_UNIT'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personadoptpractice_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personadoptpractice_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']"})
        },
        'dashboard.persongroups': {
            'Meta': {'unique_together': "(('group_name', 'village'),)", 'object_name': 'PersonGroups', 'db_table': "u'PERSON_GROUPS'"},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'DAYS'", 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'GROUP_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'TIME_UPDATED'", 'blank': 'True'}),
            'timings': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'TIMINGS'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'persongroups_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'persongroups_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personmeetingattendance': {
            'Meta': {'object_name': 'PersonMeetingAttendance', 'db_table': "u'PERSON_MEETING_ATTENDANCE'"},
            'expressed_adoption_video': ('dashboard.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_adoption_video'", 'null': 'True', 'db_column': "'EXPRESSED_ADOPTION_VIDEO'", 'to': "orm['dashboard.Video']"}),
            'expressed_question': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_QUESTION'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'interested': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'INTERESTED'", 'db_index': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personmeetingattendance_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personmeetingattendance_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.personrelations': {
            'Meta': {'object_name': 'PersonRelations', 'db_table': "u'PERSON_RELATIONS'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'related_name': "'person'", 'to': "orm['dashboard.Person']"}),
            'relative': ('dashboard.fields.BigForeignKey', [], {'related_name': "'relative'", 'to': "orm['dashboard.Person']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'type_of_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'TYPE_OF_RELATIONSHIP'"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personrelations_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personrelations_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.personshowninvideo': {
            'Meta': {'object_name': 'PersonShownInVideo', 'db_table': "u'VIDEO_farmers_shown'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']", 'db_column': "'person_id'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personshowninvideo_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personshowninvideo_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.practices': {
            'Meta': {'unique_together': "(('practice_sector', 'practice_subsector', 'practice_topic', 'practice_subtopic', 'practice_subject'),)", 'object_name': 'Practices', 'db_table': "u'PRACTICES'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'practice_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': "'True'", 'null': 'True', 'db_column': "'PRACTICE_NAME'"}),
            'practice_sector': ('dashboard.fields.BigForeignKey', [], {'default': '1', 'to': "orm['dashboard.PracticeSector']"}),
            'practice_subject': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubject']", 'null': 'True'}),
            'practice_subsector': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubSector']", 'null': 'True'}),
            'practice_subtopic': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeSubtopic']", 'null': 'True'}),
            'practice_topic': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PracticeTopic']", 'null': 'True'}),
            'seasonality': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "'SEASONALITY'"}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practices_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practices_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesector': {
            'Meta': {'object_name': 'PracticeSector', 'db_table': "u'practice_sector'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesector_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesector_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubject': {
            'Meta': {'object_name': 'PracticeSubject', 'db_table': "u'practice_subject'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubject_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubject_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubsector': {
            'Meta': {'object_name': 'PracticeSubSector', 'db_table': "u'practice_subsector'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubsector_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubsector_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubtopic': {
            'Meta': {'object_name': 'PracticeSubtopic', 'db_table': "u'practice_subtopic'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubtopic_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubtopic_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicetopic': {
            'Meta': {'object_name': 'PracticeTopic', 'db_table': "u'practice_topic'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicetopic_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicetopic_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'REGION'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.regiontest': {
            'Meta': {'object_name': 'RegionTest', 'db_table': "u'REGION_TEST'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'regiontest_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'regiontest_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.reviewer': {
            'Meta': {'object_name': 'Reviewer', 'db_table': "u'REVIEWER'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_msg': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rule_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rule_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.screening': {
            'Meta': {'unique_together': "(('date', 'start_time', 'end_time', 'location', 'village'),)", 'object_name': 'Screening', 'db_table': "u'SCREENING'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'db_column': "'END_TIME'"}),
            'farmer_groups_targeted': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.PersonGroups']", 'symmetrical': 'False'}),
            'farmers_attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Person']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'LOCATION'", 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'db_column': "'START_TIME'"}),
            'target_adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_ADOPTIONS'", 'blank': 'True'}),
            'target_audience_interest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_AUDIENCE_INTEREST'", 'blank': 'True'}),
            'target_person_attendance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_PERSON_ATTENDANCE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'screening_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'screening_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'videoes_screened': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Video']", 'symmetrical': 'False'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.state': {
            'Meta': {'object_name': 'State', 'db_table': "u'STATE'"},
            'country': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Country']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'STATE_NAME'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
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
            'Meta': {'unique_together': "(('training_start_date', 'training_end_date', 'village'),)", 'object_name': 'Training', 'db_table': "u'TRAINING'"},
            'animators_trained': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Animator']", 'symmetrical': 'False'}),
            'development_manager_present': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.DevelopmentManager']", 'null': 'True', 'db_column': "'dm_id'", 'blank': 'True'}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'db_column': "'fieldofficer_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'training_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_END_DATE'"}),
            'training_outcome': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_OUTCOME'", 'blank': 'True'}),
            'training_purpose': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_PURPOSE'", 'blank': 'True'}),
            'training_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_START_DATE'"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.traininganimatorstrained': {
            'Meta': {'object_name': 'TrainingAnimatorsTrained', 'db_table': "u'TRAINING_animators_trained'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']", 'db_column': "'animator_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'training': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Training']", 'db_column': "'training_id'"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'traininganimatorstrained_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'traininganimatorstrained_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'district_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userpermission_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userpermission_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.video': {
            'Meta': {'unique_together': "(('title', 'video_production_start_date', 'video_production_end_date', 'village'),)", 'object_name': 'Video', 'db_table': "u'VIDEO'"},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'ACTORS'"}),
            'approval_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'APPROVAL_DATE'", 'blank': 'True'}),
            'audio_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'AUDIO_QUALITY'", 'blank': 'True'}),
            'cameraoperator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'cameraoperator'", 'to': "orm['dashboard.Animator']"}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'DURATION'", 'blank': 'True'}),
            'edit_finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_FINISH_DATE'", 'blank': 'True'}),
            'edit_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_START_DATE'", 'blank': 'True'}),
            'editing_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'EDITING_QUALITY'", 'blank': 'True'}),
            'facilitator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'facilitator'", 'to': "orm['dashboard.Animator']"}),
            'farmers_shown': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Person']", 'symmetrical': 'False'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'TITLE'"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'video_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video_production_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_END_DATE'"}),
            'video_production_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_START_DATE'"}),
            'video_suitable_for': ('django.db.models.fields.IntegerField', [], {'db_column': "'VIDEO_SUITABLE_FOR'"}),
            'video_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'VIDEO_TYPE'"}),
            'viewers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"}),
            'youtubeid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'YOUTUBEID'", 'blank': 'True'})
        },
        'dashboard.videosscreenedinscreening': {
            'Meta': {'object_name': 'VideosScreenedInScreening', 'db_table': "u'SCREENING_videoes_screened'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videosscreenedinscreening_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videosscreenedinscreening_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village', 'db_table': "u'VILLAGE'"},
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        },
        'dashboard.villageprecalculation': {
            'Meta': {'unique_together': "(('village', 'date'),)", 'object_name': 'VillagePrecalculation', 'db_table': "u'village_precalculation'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'TIME_CREATED'", 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_column': "'TIME_MODIFIED'", 'blank': 'True'}),
            'total_active_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adopted_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adoption_by_active': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villageprecalculation_related_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villageprecalculation_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        }
    }

    complete_apps = ['dashboard']
