# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.user_created'
        db.add_column(u'person', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='person_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Person.time_created'
        db.add_column(u'person', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.user_modified'
        db.add_column(u'person', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='person_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Person.time_modified'
        db.add_column(u'person', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Target.user_created'
        db.add_column('dashboard_target', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='target_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Target.time_created'
        db.add_column('dashboard_target', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Target.user_modified'
        db.add_column('dashboard_target', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='target_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Target.time_modified'
        db.add_column('dashboard_target', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DevelopmentManager.user_created'
        db.add_column(u'development_manager', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='developmentmanager_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'DevelopmentManager.time_created'
        db.add_column(u'development_manager', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DevelopmentManager.user_modified'
        db.add_column(u'development_manager', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='developmentmanager_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'DevelopmentManager.time_modified'
        db.add_column(u'development_manager', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'State.user_created'
        db.add_column(u'state', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='state_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'State.time_created'
        db.add_column(u'state', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'State.user_modified'
        db.add_column(u'state', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='state_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'State.time_modified'
        db.add_column(u'state', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonAdoptPractice.user_created'
        db.add_column(u'person_adopt_practice', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personadoptpractice_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PersonAdoptPractice.time_created'
        db.add_column(u'person_adopt_practice', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonAdoptPractice.user_modified'
        db.add_column(u'person_adopt_practice', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personadoptpractice_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PersonAdoptPractice.time_modified'
        db.add_column(u'person_adopt_practice', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonAdoptPractice.time_updated'
        db.add_column(u'person_adopt_practice', 'time_updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Video.user_created'
        db.add_column(u'video', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='video_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Video.time_created'
        db.add_column(u'video', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Video.user_modified'
        db.add_column(u'video', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='video_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Video.time_modified'
        db.add_column(u'video', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Region.user_created'
        db.add_column(u'region', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='region_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Region.time_created'
        db.add_column(u'region', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Region.user_modified'
        db.add_column(u'region', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='region_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Region.time_modified'
        db.add_column(u'region', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Animator.user_created'
        db.add_column(u'animator', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animator_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Animator.time_created'
        db.add_column(u'animator', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Animator.user_modified'
        db.add_column(u'animator', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animator_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Animator.time_modified'
        db.add_column(u'animator', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RegionTest.user_created'
        db.add_column(u'region_test', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='regiontest_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'RegionTest.time_created'
        db.add_column(u'region_test', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RegionTest.user_modified'
        db.add_column(u'region_test', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='regiontest_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'RegionTest.time_modified'
        db.add_column(u'region_test', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.user_created'
        db.add_column(u'animator_salary_per_month', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorsalarypermonth_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.time_created'
        db.add_column(u'animator_salary_per_month', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.user_modified'
        db.add_column(u'animator_salary_per_month', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorsalarypermonth_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AnimatorSalaryPerMonth.time_modified'
        db.add_column(u'animator_salary_per_month', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Rule.user_created'
        db.add_column('dashboard_rule', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rule_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Rule.time_created'
        db.add_column('dashboard_rule', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Rule.user_modified'
        db.add_column('dashboard_rule', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rule_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Rule.time_modified'
        db.add_column('dashboard_rule', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partners.user_created'
        db.add_column(u'partners', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='partners_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Partners.time_created'
        db.add_column(u'partners', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Partners.user_modified'
        db.add_column(u'partners', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='partners_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Partners.time_modified'
        db.add_column(u'partners', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Training.user_created'
        db.add_column(u'training', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='training_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Training.time_created'
        db.add_column(u'training', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Training.user_modified'
        db.add_column(u'training', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='training_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Training.time_modified'
        db.add_column(u'training', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSector.user_created'
        db.add_column(u'practice_sector', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesector_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSector.time_created'
        db.add_column(u'practice_sector', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSector.user_modified'
        db.add_column(u'practice_sector', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesector_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSector.time_modified'
        db.add_column(u'practice_sector', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserPermission.user_created'
        db.add_column('dashboard_userpermission', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userpermission_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'UserPermission.time_created'
        db.add_column('dashboard_userpermission', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserPermission.user_modified'
        db.add_column('dashboard_userpermission', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userpermission_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'UserPermission.time_modified'
        db.add_column('dashboard_userpermission', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Language.user_created'
        db.add_column(u'language', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='language_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Language.time_created'
        db.add_column(u'language', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Language.user_modified'
        db.add_column(u'language', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='language_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Language.time_modified'
        db.add_column(u'language', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Error.user_created'
        db.add_column('dashboard_error', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='error_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Error.time_created'
        db.add_column('dashboard_error', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Error.user_modified'
        db.add_column('dashboard_error', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='error_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Error.time_modified'
        db.add_column('dashboard_error', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reviewer.user_created'
        db.add_column(u'reviewer', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reviewer_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Reviewer.time_created'
        db.add_column(u'reviewer', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reviewer.user_modified'
        db.add_column(u'reviewer', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reviewer_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Reviewer.time_modified'
        db.add_column(u'reviewer', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSubtopic.user_created'
        db.add_column(u'practice_subtopic', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubtopic_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSubtopic.time_created'
        db.add_column(u'practice_subtopic', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSubtopic.user_modified'
        db.add_column(u'practice_subtopic', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubtopic_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSubtopic.time_modified'
        db.add_column(u'practice_subtopic', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MonthlyCostPerVillage.user_created'
        db.add_column(u'monthly_cost_per_village', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='monthlycostpervillage_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'MonthlyCostPerVillage.time_created'
        db.add_column(u'monthly_cost_per_village', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MonthlyCostPerVillage.user_modified'
        db.add_column(u'monthly_cost_per_village', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='monthlycostpervillage_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'MonthlyCostPerVillage.time_modified'
        db.add_column(u'monthly_cost_per_village', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VillagePrecalculation.user_created'
        db.add_column(u'village_precalculation', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='villageprecalculation_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'VillagePrecalculation.time_created'
        db.add_column(u'village_precalculation', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VillagePrecalculation.user_modified'
        db.add_column(u'village_precalculation', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='villageprecalculation_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'VillagePrecalculation.time_modified'
        db.add_column(u'village_precalculation', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSubSector.user_created'
        db.add_column(u'practice_subsector', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubsector_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSubSector.time_created'
        db.add_column(u'practice_subsector', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSubSector.user_modified'
        db.add_column(u'practice_subsector', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubsector_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSubSector.time_modified'
        db.add_column(u'practice_subsector', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Equipment.user_created'
        db.add_column(u'equipment_id', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipment_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Equipment.time_created'
        db.add_column(u'equipment_id', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Equipment.user_modified'
        db.add_column(u'equipment_id', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipment_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Equipment.time_modified'
        db.add_column(u'equipment_id', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'FieldOfficer.user_created'
        db.add_column(u'field_officer', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fieldofficer_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'FieldOfficer.time_created'
        db.add_column(u'field_officer', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'FieldOfficer.user_modified'
        db.add_column(u'field_officer', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fieldofficer_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'FieldOfficer.time_modified'
        db.add_column(u'field_officer', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.user_created'
        db.add_column(u'country', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='country_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Country.time_created'
        db.add_column(u'country', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Country.user_modified'
        db.add_column(u'country', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='country_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Country.time_modified'
        db.add_column(u'country', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Block.user_created'
        db.add_column(u'block', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='block_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Block.time_created'
        db.add_column(u'block', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Block.user_modified'
        db.add_column(u'block', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='block_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Block.time_modified'
        db.add_column(u'block', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Village.user_created'
        db.add_column(u'village', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='village_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Village.time_created'
        db.add_column(u'village', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Village.user_modified'
        db.add_column(u'village', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='village_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Village.time_modified'
        db.add_column(u'village', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Screening.user_created'
        db.add_column(u'screening', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='screening_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Screening.time_created'
        db.add_column(u'screening', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Screening.user_modified'
        db.add_column(u'screening', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='screening_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Screening.time_modified'
        db.add_column(u'screening', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSubject.user_created'
        db.add_column(u'practice_subject', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubject_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSubject.time_created'
        db.add_column(u'practice_subject', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeSubject.user_modified'
        db.add_column(u'practice_subject', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicesubject_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeSubject.time_modified'
        db.add_column(u'practice_subject', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'OfflineUser.user_created'
        db.add_column('dashboard_offlineuser', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='offlineuser_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'OfflineUser.time_created'
        db.add_column('dashboard_offlineuser', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'OfflineUser.user_modified'
        db.add_column('dashboard_offlineuser', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='offlineuser_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'OfflineUser.time_modified'
        db.add_column('dashboard_offlineuser', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonMeetingAttendance.user_created'
        db.add_column(u'person_meeting_attendance', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personmeetingattendance_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PersonMeetingAttendance.time_created'
        db.add_column(u'person_meeting_attendance', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonMeetingAttendance.user_modified'
        db.add_column(u'person_meeting_attendance', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='personmeetingattendance_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PersonMeetingAttendance.time_modified'
        db.add_column(u'person_meeting_attendance', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'EquipmentHolder.user_created'
        db.add_column(u'equipment_holder', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipmentholder_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'EquipmentHolder.time_created'
        db.add_column(u'equipment_holder', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'EquipmentHolder.user_modified'
        db.add_column(u'equipment_holder', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipmentholder_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'EquipmentHolder.time_modified'
        db.add_column(u'equipment_holder', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AnimatorAssignedVillage.user_created'
        db.add_column(u'animator_assigned_village', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorassignedvillage_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AnimatorAssignedVillage.time_created'
        db.add_column(u'animator_assigned_village', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AnimatorAssignedVillage.user_modified'
        db.add_column(u'animator_assigned_village', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animatorassignedvillage_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AnimatorAssignedVillage.time_modified'
        db.add_column(u'animator_assigned_village', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeTopic.user_created'
        db.add_column(u'practice_topic', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicetopic_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeTopic.time_created'
        db.add_column(u'practice_topic', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PracticeTopic.user_modified'
        db.add_column(u'practice_topic', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practicetopic_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PracticeTopic.time_modified'
        db.add_column(u'practice_topic', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Practices.user_created'
        db.add_column(u'practices', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practices_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Practices.time_created'
        db.add_column(u'practices', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Practices.user_modified'
        db.add_column(u'practices', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='practices_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Practices.time_modified'
        db.add_column(u'practices', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'District.user_created'
        db.add_column(u'district', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='district_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'District.time_created'
        db.add_column(u'district', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'District.user_modified'
        db.add_column(u'district', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='district_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'District.time_modified'
        db.add_column(u'district', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonGroups.user_created'
        db.add_column(u'person_groups', 'user_created',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='persongroups_created', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PersonGroups.time_created'
        db.add_column(u'person_groups', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PersonGroups.user_modified'
        db.add_column(u'person_groups', 'user_modified',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='persongroups_related_modified', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'PersonGroups.time_modified'
        db.add_column(u'person_groups', 'time_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.user_created'
        db.delete_column(u'person', 'user_created_id')

        # Deleting field 'Person.time_created'
        db.delete_column(u'person', 'time_created')

        # Deleting field 'Person.user_modified'
        db.delete_column(u'person', 'user_modified_id')

        # Deleting field 'Person.time_modified'
        db.delete_column(u'person', 'time_modified')

        # Deleting field 'Target.user_created'
        db.delete_column('dashboard_target', 'user_created_id')

        # Deleting field 'Target.time_created'
        db.delete_column('dashboard_target', 'time_created')

        # Deleting field 'Target.user_modified'
        db.delete_column('dashboard_target', 'user_modified_id')

        # Deleting field 'Target.time_modified'
        db.delete_column('dashboard_target', 'time_modified')

        # Deleting field 'DevelopmentManager.user_created'
        db.delete_column(u'development_manager', 'user_created_id')

        # Deleting field 'DevelopmentManager.time_created'
        db.delete_column(u'development_manager', 'time_created')

        # Deleting field 'DevelopmentManager.user_modified'
        db.delete_column(u'development_manager', 'user_modified_id')

        # Deleting field 'DevelopmentManager.time_modified'
        db.delete_column(u'development_manager', 'time_modified')

        # Deleting field 'State.user_created'
        db.delete_column(u'state', 'user_created_id')

        # Deleting field 'State.time_created'
        db.delete_column(u'state', 'time_created')

        # Deleting field 'State.user_modified'
        db.delete_column(u'state', 'user_modified_id')

        # Deleting field 'State.time_modified'
        db.delete_column(u'state', 'time_modified')

        # Deleting field 'PersonAdoptPractice.user_created'
        db.delete_column(u'person_adopt_practice', 'user_created_id')

        # Deleting field 'PersonAdoptPractice.time_created'
        db.delete_column(u'person_adopt_practice', 'time_created')

        # Deleting field 'PersonAdoptPractice.user_modified'
        db.delete_column(u'person_adopt_practice', 'user_modified_id')

        # Deleting field 'PersonAdoptPractice.time_modified'
        db.delete_column(u'person_adopt_practice', 'time_modified')

        # Deleting field 'PersonAdoptPractice.time_updated'
        db.delete_column(u'person_adopt_practice', 'time_updated')

        # Deleting field 'Video.user_created'
        db.delete_column(u'video', 'user_created_id')

        # Deleting field 'Video.time_created'
        db.delete_column(u'video', 'time_created')

        # Deleting field 'Video.user_modified'
        db.delete_column(u'video', 'user_modified_id')

        # Deleting field 'Video.time_modified'
        db.delete_column(u'video', 'time_modified')

        # Deleting field 'Region.user_created'
        db.delete_column(u'region', 'user_created_id')

        # Deleting field 'Region.time_created'
        db.delete_column(u'region', 'time_created')

        # Deleting field 'Region.user_modified'
        db.delete_column(u'region', 'user_modified_id')

        # Deleting field 'Region.time_modified'
        db.delete_column(u'region', 'time_modified')

        # Deleting field 'Animator.user_created'
        db.delete_column(u'animator', 'user_created_id')

        # Deleting field 'Animator.time_created'
        db.delete_column(u'animator', 'time_created')

        # Deleting field 'Animator.user_modified'
        db.delete_column(u'animator', 'user_modified_id')

        # Deleting field 'Animator.time_modified'
        db.delete_column(u'animator', 'time_modified')

        # Deleting field 'RegionTest.user_created'
        db.delete_column(u'region_test', 'user_created_id')

        # Deleting field 'RegionTest.time_created'
        db.delete_column(u'region_test', 'time_created')

        # Deleting field 'RegionTest.user_modified'
        db.delete_column(u'region_test', 'user_modified_id')

        # Deleting field 'RegionTest.time_modified'
        db.delete_column(u'region_test', 'time_modified')

        # Deleting field 'AnimatorSalaryPerMonth.user_created'
        db.delete_column(u'animator_salary_per_month', 'user_created_id')

        # Deleting field 'AnimatorSalaryPerMonth.time_created'
        db.delete_column(u'animator_salary_per_month', 'time_created')

        # Deleting field 'AnimatorSalaryPerMonth.user_modified'
        db.delete_column(u'animator_salary_per_month', 'user_modified_id')

        # Deleting field 'AnimatorSalaryPerMonth.time_modified'
        db.delete_column(u'animator_salary_per_month', 'time_modified')

        # Deleting field 'Rule.user_created'
        db.delete_column('dashboard_rule', 'user_created_id')

        # Deleting field 'Rule.time_created'
        db.delete_column('dashboard_rule', 'time_created')

        # Deleting field 'Rule.user_modified'
        db.delete_column('dashboard_rule', 'user_modified_id')

        # Deleting field 'Rule.time_modified'
        db.delete_column('dashboard_rule', 'time_modified')

        # Deleting field 'Partners.user_created'
        db.delete_column(u'partners', 'user_created_id')

        # Deleting field 'Partners.time_created'
        db.delete_column(u'partners', 'time_created')

        # Deleting field 'Partners.user_modified'
        db.delete_column(u'partners', 'user_modified_id')

        # Deleting field 'Partners.time_modified'
        db.delete_column(u'partners', 'time_modified')

        # Deleting field 'Training.user_created'
        db.delete_column(u'training', 'user_created_id')

        # Deleting field 'Training.time_created'
        db.delete_column(u'training', 'time_created')

        # Deleting field 'Training.user_modified'
        db.delete_column(u'training', 'user_modified_id')

        # Deleting field 'Training.time_modified'
        db.delete_column(u'training', 'time_modified')

        # Deleting field 'PracticeSector.user_created'
        db.delete_column(u'practice_sector', 'user_created_id')

        # Deleting field 'PracticeSector.time_created'
        db.delete_column(u'practice_sector', 'time_created')

        # Deleting field 'PracticeSector.user_modified'
        db.delete_column(u'practice_sector', 'user_modified_id')

        # Deleting field 'PracticeSector.time_modified'
        db.delete_column(u'practice_sector', 'time_modified')

        # Deleting field 'UserPermission.user_created'
        db.delete_column('dashboard_userpermission', 'user_created_id')

        # Deleting field 'UserPermission.time_created'
        db.delete_column('dashboard_userpermission', 'time_created')

        # Deleting field 'UserPermission.user_modified'
        db.delete_column('dashboard_userpermission', 'user_modified_id')

        # Deleting field 'UserPermission.time_modified'
        db.delete_column('dashboard_userpermission', 'time_modified')

        # Deleting field 'Language.user_created'
        db.delete_column(u'language', 'user_created_id')

        # Deleting field 'Language.time_created'
        db.delete_column(u'language', 'time_created')

        # Deleting field 'Language.user_modified'
        db.delete_column(u'language', 'user_modified_id')

        # Deleting field 'Language.time_modified'
        db.delete_column(u'language', 'time_modified')

        # Deleting field 'Error.user_created'
        db.delete_column('dashboard_error', 'user_created_id')

        # Deleting field 'Error.time_created'
        db.delete_column('dashboard_error', 'time_created')

        # Deleting field 'Error.user_modified'
        db.delete_column('dashboard_error', 'user_modified_id')

        # Deleting field 'Error.time_modified'
        db.delete_column('dashboard_error', 'time_modified')

        # Deleting field 'Reviewer.user_created'
        db.delete_column(u'reviewer', 'user_created_id')

        # Deleting field 'Reviewer.time_created'
        db.delete_column(u'reviewer', 'time_created')

        # Deleting field 'Reviewer.user_modified'
        db.delete_column(u'reviewer', 'user_modified_id')

        # Deleting field 'Reviewer.time_modified'
        db.delete_column(u'reviewer', 'time_modified')

        # Deleting field 'PracticeSubtopic.user_created'
        db.delete_column(u'practice_subtopic', 'user_created_id')

        # Deleting field 'PracticeSubtopic.time_created'
        db.delete_column(u'practice_subtopic', 'time_created')

        # Deleting field 'PracticeSubtopic.user_modified'
        db.delete_column(u'practice_subtopic', 'user_modified_id')

        # Deleting field 'PracticeSubtopic.time_modified'
        db.delete_column(u'practice_subtopic', 'time_modified')

        # Deleting field 'MonthlyCostPerVillage.user_created'
        db.delete_column(u'monthly_cost_per_village', 'user_created_id')

        # Deleting field 'MonthlyCostPerVillage.time_created'
        db.delete_column(u'monthly_cost_per_village', 'time_created')

        # Deleting field 'MonthlyCostPerVillage.user_modified'
        db.delete_column(u'monthly_cost_per_village', 'user_modified_id')

        # Deleting field 'MonthlyCostPerVillage.time_modified'
        db.delete_column(u'monthly_cost_per_village', 'time_modified')

        # Deleting field 'VillagePrecalculation.user_created'
        db.delete_column(u'village_precalculation', 'user_created_id')

        # Deleting field 'VillagePrecalculation.time_created'
        db.delete_column(u'village_precalculation', 'time_created')

        # Deleting field 'VillagePrecalculation.user_modified'
        db.delete_column(u'village_precalculation', 'user_modified_id')

        # Deleting field 'VillagePrecalculation.time_modified'
        db.delete_column(u'village_precalculation', 'time_modified')

        # Deleting field 'PracticeSubSector.user_created'
        db.delete_column(u'practice_subsector', 'user_created_id')

        # Deleting field 'PracticeSubSector.time_created'
        db.delete_column(u'practice_subsector', 'time_created')

        # Deleting field 'PracticeSubSector.user_modified'
        db.delete_column(u'practice_subsector', 'user_modified_id')

        # Deleting field 'PracticeSubSector.time_modified'
        db.delete_column(u'practice_subsector', 'time_modified')

        # Deleting field 'Equipment.user_created'
        db.delete_column(u'equipment_id', 'user_created_id')

        # Deleting field 'Equipment.time_created'
        db.delete_column(u'equipment_id', 'time_created')

        # Deleting field 'Equipment.user_modified'
        db.delete_column(u'equipment_id', 'user_modified_id')

        # Deleting field 'Equipment.time_modified'
        db.delete_column(u'equipment_id', 'time_modified')

        # Deleting field 'FieldOfficer.user_created'
        db.delete_column(u'field_officer', 'user_created_id')

        # Deleting field 'FieldOfficer.time_created'
        db.delete_column(u'field_officer', 'time_created')

        # Deleting field 'FieldOfficer.user_modified'
        db.delete_column(u'field_officer', 'user_modified_id')

        # Deleting field 'FieldOfficer.time_modified'
        db.delete_column(u'field_officer', 'time_modified')

        # Deleting field 'Country.user_created'
        db.delete_column(u'country', 'user_created_id')

        # Deleting field 'Country.time_created'
        db.delete_column(u'country', 'time_created')

        # Deleting field 'Country.user_modified'
        db.delete_column(u'country', 'user_modified_id')

        # Deleting field 'Country.time_modified'
        db.delete_column(u'country', 'time_modified')

        # Deleting field 'Block.user_created'
        db.delete_column(u'block', 'user_created_id')

        # Deleting field 'Block.time_created'
        db.delete_column(u'block', 'time_created')

        # Deleting field 'Block.user_modified'
        db.delete_column(u'block', 'user_modified_id')

        # Deleting field 'Block.time_modified'
        db.delete_column(u'block', 'time_modified')

        # Deleting field 'Village.user_created'
        db.delete_column(u'village', 'user_created_id')

        # Deleting field 'Village.time_created'
        db.delete_column(u'village', 'time_created')

        # Deleting field 'Village.user_modified'
        db.delete_column(u'village', 'user_modified_id')

        # Deleting field 'Village.time_modified'
        db.delete_column(u'village', 'time_modified')

        # Deleting field 'Screening.user_created'
        db.delete_column(u'screening', 'user_created_id')

        # Deleting field 'Screening.time_created'
        db.delete_column(u'screening', 'time_created')

        # Deleting field 'Screening.user_modified'
        db.delete_column(u'screening', 'user_modified_id')

        # Deleting field 'Screening.time_modified'
        db.delete_column(u'screening', 'time_modified')

        # Deleting field 'PracticeSubject.user_created'
        db.delete_column(u'practice_subject', 'user_created_id')

        # Deleting field 'PracticeSubject.time_created'
        db.delete_column(u'practice_subject', 'time_created')

        # Deleting field 'PracticeSubject.user_modified'
        db.delete_column(u'practice_subject', 'user_modified_id')

        # Deleting field 'PracticeSubject.time_modified'
        db.delete_column(u'practice_subject', 'time_modified')

        # Deleting field 'OfflineUser.user_created'
        db.delete_column('dashboard_offlineuser', 'user_created_id')

        # Deleting field 'OfflineUser.time_created'
        db.delete_column('dashboard_offlineuser', 'time_created')

        # Deleting field 'OfflineUser.user_modified'
        db.delete_column('dashboard_offlineuser', 'user_modified_id')

        # Deleting field 'OfflineUser.time_modified'
        db.delete_column('dashboard_offlineuser', 'time_modified')

        # Deleting field 'PersonMeetingAttendance.user_created'
        db.delete_column(u'person_meeting_attendance', 'user_created_id')

        # Deleting field 'PersonMeetingAttendance.time_created'
        db.delete_column(u'person_meeting_attendance', 'time_created')

        # Deleting field 'PersonMeetingAttendance.user_modified'
        db.delete_column(u'person_meeting_attendance', 'user_modified_id')

        # Deleting field 'PersonMeetingAttendance.time_modified'
        db.delete_column(u'person_meeting_attendance', 'time_modified')

        # Deleting field 'EquipmentHolder.user_created'
        db.delete_column(u'equipment_holder', 'user_created_id')

        # Deleting field 'EquipmentHolder.time_created'
        db.delete_column(u'equipment_holder', 'time_created')

        # Deleting field 'EquipmentHolder.user_modified'
        db.delete_column(u'equipment_holder', 'user_modified_id')

        # Deleting field 'EquipmentHolder.time_modified'
        db.delete_column(u'equipment_holder', 'time_modified')

        # Deleting field 'AnimatorAssignedVillage.user_created'
        db.delete_column(u'animator_assigned_village', 'user_created_id')

        # Deleting field 'AnimatorAssignedVillage.time_created'
        db.delete_column(u'animator_assigned_village', 'time_created')

        # Deleting field 'AnimatorAssignedVillage.user_modified'
        db.delete_column(u'animator_assigned_village', 'user_modified_id')

        # Deleting field 'AnimatorAssignedVillage.time_modified'
        db.delete_column(u'animator_assigned_village', 'time_modified')

        # Deleting field 'PracticeTopic.user_created'
        db.delete_column(u'practice_topic', 'user_created_id')

        # Deleting field 'PracticeTopic.time_created'
        db.delete_column(u'practice_topic', 'time_created')

        # Deleting field 'PracticeTopic.user_modified'
        db.delete_column(u'practice_topic', 'user_modified_id')

        # Deleting field 'PracticeTopic.time_modified'
        db.delete_column(u'practice_topic', 'time_modified')

        # Deleting field 'Practices.user_created'
        db.delete_column(u'practices', 'user_created_id')

        # Deleting field 'Practices.time_created'
        db.delete_column(u'practices', 'time_created')

        # Deleting field 'Practices.user_modified'
        db.delete_column(u'practices', 'user_modified_id')

        # Deleting field 'Practices.time_modified'
        db.delete_column(u'practices', 'time_modified')

        # Deleting field 'District.user_created'
        db.delete_column(u'district', 'user_created_id')

        # Deleting field 'District.time_created'
        db.delete_column(u'district', 'time_created')

        # Deleting field 'District.user_modified'
        db.delete_column(u'district', 'user_modified_id')

        # Deleting field 'District.time_modified'
        db.delete_column(u'district', 'time_modified')

        # Deleting field 'PersonGroups.user_created'
        db.delete_column(u'person_groups', 'user_created_id')

        # Deleting field 'PersonGroups.time_created'
        db.delete_column(u'person_groups', 'time_created')

        # Deleting field 'PersonGroups.user_modified'
        db.delete_column(u'person_groups', 'user_modified_id')

        # Deleting field 'PersonGroups.time_modified'
        db.delete_column(u'person_groups', 'time_modified')


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
        'dashboard.animatorsalarypermonth': {
            'Meta': {'object_name': 'AnimatorSalaryPerMonth', 'db_table': "u'animator_salary_per_month'"},
            'animator': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'pay_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PAY_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'total_salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_SALARY'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorsalarypermonth_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animatorsalarypermonth_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
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
        'dashboard.equipment': {
            'Meta': {'object_name': 'Equipment', 'db_table': "u'equipment_id'"},
            'additional_accessories': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COST'", 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.IntegerField', [], {'db_column': "'EQUIPMENT_TYPE'"}),
            'equipmentholder': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.EquipmentHolder']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'installation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'INVOICE_NO'"}),
            'is_reserve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'MODEL_NO'", 'blank': 'True'}),
            'other_equipment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'db_column': "'OTHER_EQUIPMENT'", 'blank': 'True'}),
            'procurement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PROCUREMENT_DATE'", 'blank': 'True'}),
            'purpose': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'purpose'", 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'SERIAL_NO'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'transfer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipment_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipment_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'null': 'True', 'blank': 'True'}),
            'warranty_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'WARRANTY_EXPIRATION_DATE'", 'blank': 'True'})
        },
        'dashboard.equipmentholder': {
            'Meta': {'object_name': 'EquipmentHolder', 'db_table': "u'equipment_holder'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipmentholder_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipmentholder_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
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
        'dashboard.language': {
            'Meta': {'object_name': 'Language', 'db_table': "u'language'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.monthlycostpervillage': {
            'Meta': {'object_name': 'MonthlyCostPerVillage', 'db_table': "u'monthly_cost_per_village'"},
            'community_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COMMUNITY_COST'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'digitalgreen_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'DIGITALGREEN_COST'", 'blank': 'True'}),
            'equipment_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'EQUIPMENT_COST'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'labor_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LABOR_COST'", 'blank': 'True'}),
            'miscellaneous_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'MISCELLANEOUS_COST'", 'blank': 'True'}),
            'partners_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'PARTNERS_COST'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_COST'", 'blank': 'True'}),
            'transportation_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TRANSPORTATION_COST'", 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'monthlycostpervillage_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'monthlycostpervillage_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
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
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rel'", 'to': "orm['dashboard.Person']", 'through': "orm['dashboard.PersonRelations']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
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
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
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
            'expressed_adoption_video': ('dashboard.fields.related.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_adoption_video'", 'null': 'True', 'db_column': "'EXPRESSED_ADOPTION_VIDEO'", 'to': "orm['dashboard.Video']"}),
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
        'dashboard.personrelations': {
            'Meta': {'object_name': 'PersonRelations', 'db_table': "u'person_relations'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.related.BigForeignKey', [], {'related_name': "'person'", 'to': "orm['dashboard.Person']"}),
            'relative': ('dashboard.fields.related.BigForeignKey', [], {'related_name': "'relative'", 'to': "orm['dashboard.Person']"}),
            'type_of_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'TYPE_OF_RELATIONSHIP'"})
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
            'seasonality': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "'SEASONALITY'"}),
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
        'dashboard.regiontest': {
            'Meta': {'object_name': 'RegionTest', 'db_table': "u'region_test'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'regiontest_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'regiontest_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
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
            'Meta': {'unique_together': "(('date', 'start_time', 'end_time', 'location', 'village'),)", 'object_name': 'Screening', 'db_table': "u'screening'"},
            'animator': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'db_column': "'END_TIME'"}),
            'farmer_groups_targeted': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.PersonGroups']", 'symmetrical': 'False'}),
            'farmers_attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Person']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'fieldofficer': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'LOCATION'", 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'db_column': "'START_TIME'"}),
            'target_adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_ADOPTIONS'", 'blank': 'True'}),
            'target_audience_interest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_AUDIENCE_INTEREST'", 'blank': 'True'}),
            'target_person_attendance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_PERSON_ATTENDANCE'", 'blank': 'True'}),
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
            'district': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'editor_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'editor_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exp_interest_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'month_year': ('django.db.models.fields.DateField', [], {}),
            'storyboard_preparation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'support_requested': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target_created'", 'null': 'True', 'to': "orm['auth.User']"}),
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
            'Meta': {'unique_together': "(('training_start_date', 'training_end_date', 'village'),)", 'object_name': 'Training', 'db_table': "u'training'"},
            'animators_trained': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.Animator']", 'symmetrical': 'False'}),
            'development_manager_present': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.DevelopmentManager']", 'null': 'True', 'db_column': "'dm_id'", 'blank': 'True'}),
            'fieldofficer': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'db_column': "'fieldofficer_id'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'training_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_END_DATE'"}),
            'training_outcome': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_OUTCOME'", 'blank': 'True'}),
            'training_purpose': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_PURPOSE'", 'blank': 'True'}),
            'training_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_START_DATE'"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'training_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
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
            'audio_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'AUDIO_QUALITY'", 'blank': 'True'}),
            'cameraoperator': ('dashboard.fields.related.BigForeignKey', [], {'related_name': "'cameraoperator'", 'to': "orm['dashboard.Animator']"}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'DURATION'", 'blank': 'True'}),
            'edit_finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_FINISH_DATE'", 'blank': 'True'}),
            'edit_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_START_DATE'", 'blank': 'True'}),
            'editing_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'EDITING_QUALITY'", 'blank': 'True'}),
            'facilitator': ('dashboard.fields.related.BigForeignKey', [], {'related_name': "'facilitator'", 'to': "orm['dashboard.Animator']"}),
            'farmers_shown': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.Person']", 'symmetrical': 'False'}),
            'final_edited_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'FINAL_EDITED_FILENAME'", 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Language']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'movie_maker_project_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'MOVIE_MAKER_PROJECT_FILENAME'", 'blank': 'True'}),
            'picture_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'PICTURE_QUALITY'", 'blank': 'True'}),
            'raw_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'RAW_FILENAME'", 'blank': 'True'}),
            'related_practice': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Practices']", 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'db_column': "'REMARKS'", 'blank': 'True'}),
            'reviewer': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Reviewer']", 'null': 'True', 'blank': 'True'}),
            'storybase': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'STORYBASE'"}),
            'storyboard_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'STORYBOARD_FILENAME'", 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'supplementary_video_produced': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'null': 'True', 'blank': 'True'}),
            'thematic_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'THEMATIC_QUALITY'", 'blank': 'True'}),
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
        'dashboard.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village', 'db_table': "u'village'"},
            'block': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Block']"}),
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CONTROL'", 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'no_of_households': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'NO_OF_HOUSEHOLDS'", 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'POPULATION'", 'blank': 'True'}),
            'road_connectivity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'ROAD_CONNECTIVITY'", 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        },
        'dashboard.villageprecalculation': {
            'Meta': {'unique_together': "(('village', 'date'),)", 'object_name': 'VillagePrecalculation', 'db_table': "u'village_precalculation'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'total_active_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adopted_attendees': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_adoption_by_active': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villageprecalculation_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villageprecalculation_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        }
    }

    complete_apps = ['dashboard']