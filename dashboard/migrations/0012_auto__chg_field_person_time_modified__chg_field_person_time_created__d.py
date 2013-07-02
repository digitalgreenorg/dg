# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Person', fields ['group', 'father_name', 'person_name', 'village']
        #db.delete_unique(u'person', ['group_id', 'FATHER_NAME', 'PERSON_NAME', 'village_id'])


        # Changing field 'Person.time_modified'
        db.alter_column(u'person', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Person.time_created'
        db.alter_column(u'person', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))
        # Adding unique constraint on 'Person', fields ['father_name', 'person_name', 'village']
        #db.create_unique(u'person', ['FATHER_NAME', 'PERSON_NAME', 'village_id'])


        # Changing field 'DevelopmentManager.time_modified'
        db.alter_column(u'development_manager', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'DevelopmentManager.time_created'
        db.alter_column(u'development_manager', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'State.time_modified'
        db.alter_column(u'state', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'State.time_created'
        db.alter_column(u'state', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PersonAdoptPractice.time_modified'
        db.alter_column(u'person_adopt_practice', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PersonAdoptPractice.time_created'
        db.alter_column(u'person_adopt_practice', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Video.time_created'
        db.alter_column(u'video', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Video.time_modified'
        db.alter_column(u'video', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Animator.time_modified'
        db.alter_column(u'animator', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Animator.time_created'
        db.alter_column(u'animator', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Rule.time_created'
        db.alter_column('dashboard_rule', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Rule.time_modified'
        db.alter_column('dashboard_rule', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Partners.time_created'
        db.alter_column(u'partners', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Partners.time_modified'
        db.alter_column(u'partners', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSector.time_modified'
        db.alter_column(u'practice_sector', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSector.time_created'
        db.alter_column(u'practice_sector', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'UserPermission.time_modified'
        db.alter_column('dashboard_userpermission', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'UserPermission.time_created'
        db.alter_column('dashboard_userpermission', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Language.time_created'
        db.alter_column(u'language', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Language.time_modified'
        db.alter_column(u'language', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Error.time_modified'
        db.alter_column('dashboard_error', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Error.time_created'
        db.alter_column('dashboard_error', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Reviewer.time_modified'
        db.alter_column(u'reviewer', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Reviewer.time_created'
        db.alter_column(u'reviewer', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSubtopic.time_modified'
        db.alter_column(u'practice_subtopic', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSubtopic.time_created'
        db.alter_column(u'practice_subtopic', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSubSector.time_modified'
        db.alter_column(u'practice_subsector', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSubSector.time_created'
        db.alter_column(u'practice_subsector', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PersonGroups.time_modified'
        db.alter_column(u'person_groups', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PersonGroups.time_created'
        db.alter_column(u'person_groups', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FieldOfficer.time_modified'
        db.alter_column(u'field_officer', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FieldOfficer.time_created'
        db.alter_column(u'field_officer', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Region.time_created'
        db.alter_column(u'region', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Region.time_modified'
        db.alter_column(u'region', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Block.time_created'
        db.alter_column(u'block', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Block.time_modified'
        db.alter_column(u'block', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Village.time_modified'
        db.alter_column(u'village', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Village.time_created'
        db.alter_column(u'village', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Screening.time_modified'
        db.alter_column(u'screening', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Screening.time_created'
        db.alter_column(u'screening', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSubject.time_modified'
        db.alter_column(u'practice_subject', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeSubject.time_created'
        db.alter_column(u'practice_subject', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'OfflineUser.time_created'
        db.alter_column('dashboard_offlineuser', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'OfflineUser.time_modified'
        db.alter_column('dashboard_offlineuser', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PersonMeetingAttendance.time_modified'
        db.alter_column(u'person_meeting_attendance', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PersonMeetingAttendance.time_created'
        db.alter_column(u'person_meeting_attendance', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'AnimatorAssignedVillage.time_modified'
        db.alter_column(u'animator_assigned_village', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'AnimatorAssignedVillage.time_created'
        db.alter_column(u'animator_assigned_village', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeTopic.time_modified'
        db.alter_column(u'practice_topic', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PracticeTopic.time_created'
        db.alter_column(u'practice_topic', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Practices.time_modified'
        db.alter_column(u'practices', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Practices.time_created'
        db.alter_column(u'practices', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'District.time_created'
        db.alter_column(u'district', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'District.time_modified'
        db.alter_column(u'district', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Country.time_modified'
        db.alter_column(u'country', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Country.time_created'
        db.alter_column(u'country', 'time_created', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Person', fields ['father_name', 'person_name', 'village']
        db.delete_unique(u'person', ['FATHER_NAME', 'PERSON_NAME', 'village_id'])


        # Changing field 'Person.time_modified'
        db.alter_column(u'person', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Person.time_created'
        db.alter_column(u'person', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))
        # Adding unique constraint on 'Person', fields ['group', 'father_name', 'person_name', 'village']
        #db.create_unique(u'person', ['group_id', 'FATHER_NAME', 'PERSON_NAME', 'village_id'])


        # Changing field 'DevelopmentManager.time_modified'
        db.alter_column(u'development_manager', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'DevelopmentManager.time_created'
        db.alter_column(u'development_manager', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'State.time_modified'
        db.alter_column(u'state', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'State.time_created'
        db.alter_column(u'state', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'PersonAdoptPractice.time_modified'
        db.alter_column(u'person_adopt_practice', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PersonAdoptPractice.time_created'
        db.alter_column(u'person_adopt_practice', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Video.time_created'
        db.alter_column(u'video', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Video.time_modified'
        db.alter_column(u'video', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Animator.time_modified'
        db.alter_column(u'animator', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Animator.time_created'
        db.alter_column(u'animator', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Rule.time_created'
        db.alter_column('dashboard_rule', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Rule.time_modified'
        db.alter_column('dashboard_rule', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Partners.time_created'
        db.alter_column(u'partners', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Partners.time_modified'
        db.alter_column(u'partners', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PracticeSector.time_modified'
        db.alter_column(u'practice_sector', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PracticeSector.time_created'
        db.alter_column(u'practice_sector', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'UserPermission.time_modified'
        db.alter_column('dashboard_userpermission', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'UserPermission.time_created'
        db.alter_column('dashboard_userpermission', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Language.time_created'
        db.alter_column(u'language', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Language.time_modified'
        db.alter_column(u'language', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Error.time_modified'
        db.alter_column('dashboard_error', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Error.time_created'
        db.alter_column('dashboard_error', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Reviewer.time_modified'
        db.alter_column(u'reviewer', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Reviewer.time_created'
        db.alter_column(u'reviewer', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'PracticeSubtopic.time_modified'
        db.alter_column(u'practice_subtopic', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PracticeSubtopic.time_created'
        db.alter_column(u'practice_subtopic', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'PracticeSubSector.time_modified'
        db.alter_column(u'practice_subsector', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PracticeSubSector.time_created'
        db.alter_column(u'practice_subsector', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'PersonGroups.time_modified'
        db.alter_column(u'person_groups', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PersonGroups.time_created'
        db.alter_column(u'person_groups', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'FieldOfficer.time_modified'
        db.alter_column(u'field_officer', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'FieldOfficer.time_created'
        db.alter_column(u'field_officer', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Region.time_created'
        db.alter_column(u'region', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Region.time_modified'
        db.alter_column(u'region', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Block.time_created'
        db.alter_column(u'block', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Block.time_modified'
        db.alter_column(u'block', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Village.time_modified'
        db.alter_column(u'village', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Village.time_created'
        db.alter_column(u'village', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Screening.time_modified'
        db.alter_column(u'screening', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Screening.time_created'
        db.alter_column(u'screening', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'PracticeSubject.time_modified'
        db.alter_column(u'practice_subject', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PracticeSubject.time_created'
        db.alter_column(u'practice_subject', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'OfflineUser.time_created'
        db.alter_column('dashboard_offlineuser', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'OfflineUser.time_modified'
        db.alter_column('dashboard_offlineuser', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PersonMeetingAttendance.time_modified'
        db.alter_column(u'person_meeting_attendance', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PersonMeetingAttendance.time_created'
        db.alter_column(u'person_meeting_attendance', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'AnimatorAssignedVillage.time_modified'
        db.alter_column(u'animator_assigned_village', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'AnimatorAssignedVillage.time_created'
        db.alter_column(u'animator_assigned_village', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'PracticeTopic.time_modified'
        db.alter_column(u'practice_topic', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'PracticeTopic.time_created'
        db.alter_column(u'practice_topic', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'Practices.time_modified'
        db.alter_column(u'practices', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Practices.time_created'
        db.alter_column(u'practices', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'District.time_created'
        db.alter_column(u'district', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

        # Changing field 'District.time_modified'
        db.alter_column(u'district', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Country.time_modified'
        db.alter_column(u'country', 'time_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'Country.time_created'
        db.alter_column(u'country', 'time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

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
            'Meta': {'unique_together': "(('name', 'gender', 'partner'),)", 'object_name': 'Animator', 'db_table': "u'animator'"},
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_animators'", 'to': "orm['dashboard.Village']", 'through': "orm['dashboard.AnimatorAssignedVillage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'partner': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Partners']", 'blank': 'True'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'total_adoptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animator_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animator_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.animatorassignedvillage': {
            'Meta': {'object_name': 'AnimatorAssignedVillage', 'db_table': "u'animator_assigned_village'"},
            'animator': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'block_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'block_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.cocouser': {
            'Meta': {'object_name': 'CocoUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'villages': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.Village']", 'symmetrical': 'False'})
        },
        'dashboard.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            'country_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'COUNTRY_NAME'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'language_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.offlineuser': {
            'Meta': {'object_name': 'OfflineUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline_pk_id': ('dashboard.fields.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partners_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.person': {
            'Meta': {'unique_together': "(('person_name', 'father_name', 'village'),)", 'object_name': 'Person', 'db_table': "u'person'"},
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
            'screenings_attended': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Screening']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personadoptpractice_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'personadoptpractice_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'video': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Video']"})
        },
        'dashboard.persongroups': {
            'Meta': {'unique_together': "(('group_name', 'village'),)", 'object_name': 'PersonGroups', 'db_table': "u'person_groups'"},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'DAYS'", 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'GROUP_NAME'"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practices_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practices_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesector': {
            'Meta': {'object_name': 'PracticeSector', 'db_table': "u'practice_sector'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesector_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesector_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubject': {
            'Meta': {'object_name': 'PracticeSubject', 'db_table': "u'practice_subject'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubject_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubject_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubsector': {
            'Meta': {'object_name': 'PracticeSubSector', 'db_table': "u'practice_subsector'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubsector_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubsector_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicesubtopic': {
            'Meta': {'object_name': 'PracticeSubtopic', 'db_table': "u'practice_subtopic'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubtopic_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicesubtopic_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.practicetopic': {
            'Meta': {'object_name': 'PracticeTopic', 'db_table': "u'practice_topic'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicetopic_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'practicetopic_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'region'"},
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.reviewer': {
            'Meta': {'object_name': 'Reviewer', 'db_table': "u'reviewer'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.fields.PositiveBigIntegerField', [], {}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviewer_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_msg': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'screening_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'screening_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'videoes_screened': ('dashboard.fields.related.BigManyToManyField', [], {'to': "orm['dashboard.Video']", 'symmetrical': 'False'}),
            'village': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.serverlog': {
            'Meta': {'object_name': 'ServerLog'},
            'action': ('django.db.models.fields.IntegerField', [], {}),
            'entry_table': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'instance_json': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'model_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'partner': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'village': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'})
        },
        'dashboard.state': {
            'Meta': {'object_name': 'State', 'db_table': "u'state'"},
            'country': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Country']"}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'STATE_NAME'"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_related_modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'dashboard.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'district_operated': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.District']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_operated': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Region']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
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
            'animators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'animators'", 'symmetrical': 'False', 'through': "orm['dashboard.AnimatorAssignedVillage']", 'to': "orm['dashboard.Animator']"}),
            'block': ('dashboard.fields.related.BigForeignKey', [], {'to': "orm['dashboard.Block']"}),
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CONTROL'", 'blank': 'True'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.fields.BigAutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'village_related_modified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        }
    }

    complete_apps = ['dashboard']