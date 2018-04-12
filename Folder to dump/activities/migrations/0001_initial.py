# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0001_initial'),
        ('people', '0001_initial'),
        ('geographies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSLPS_Screening',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('screenig_code', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonAdoptPractice',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('date_of_adoption', models.DateField()),
                ('date_of_verification', models.DateField(null=True, blank=True)),
                ('verification_status', models.IntegerField(default=0, max_length=1, choices=[(0, b'Not Checked'), (1, b'Approved'), (2, b'Rejected')])),
                ('non_negotiable_check', models.CharField(max_length=256, null=True, blank=True)),
                ('verified_by', models.IntegerField(blank=True, max_length=1, null=True, choices=[(0, b'Digital Green'), (1, b'Partner'), (2, b'Third Party')])),
                ('animator', models.ForeignKey(blank=True, to='people.Animator', null=True)),
                ('partner', models.ForeignKey(to='programs.Partner')),
                ('person', models.ForeignKey(to='people.Person')),
                ('user_created', models.ForeignKey(related_name='activities_personadoptpractice_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_personadoptpractice_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonMeetingAttendance',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('interested', models.NullBooleanField(default=None, db_index=True)),
                ('expressed_question', models.CharField(max_length=500, blank=True)),
                ('expressed_adoption_video', models.ForeignKey(related_name='expressed_adoption_video', blank=True, to='videos.Video', null=True)),
                ('person', models.ForeignKey(to='people.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('questions_asked', models.TextField(null=True, blank=True)),
                ('observation_status', models.IntegerField(default=0, max_length=1, choices=[(0, b'Not Observed'), (1, b'Observed')])),
                ('screening_grade', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'D', b'D')])),
                ('observer', models.IntegerField(blank=True, max_length=1, null=True, choices=[(0, b'Digital Green'), (1, b'Partner'), (2, b'Third Party')])),
                ('animator', models.ForeignKey(to='people.Animator')),
                ('farmer_groups_targeted', models.ManyToManyField(to='people.PersonGroup')),
                ('farmers_attendance', models.ManyToManyField(to='people.Person', null=b'False', through='activities.PersonMeetingAttendance', blank=b'False')),
                ('partner', models.ForeignKey(to='programs.Partner')),
                ('user_created', models.ForeignKey(related_name='activities_screening_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_screening_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('videoes_screened', models.ManyToManyField(to='videos.Video')),
                ('village', models.ForeignKey(to='geographies.Village')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='screening',
            unique_together=set([('date', 'start_time', 'end_time', 'animator', 'village')]),
        ),
        migrations.AddField(
            model_name='personmeetingattendance',
            name='screening',
            field=models.ForeignKey(to='activities.Screening'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personmeetingattendance',
            name='user_created',
            field=models.ForeignKey(related_name='activities_personmeetingattendance_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personmeetingattendance',
            name='user_modified',
            field=models.ForeignKey(related_name='activities_personmeetingattendance_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='personadoptpractice',
            unique_together=set([('person', 'video', 'date_of_adoption')]),
        ),
        migrations.AddField(
            model_name='jslps_screening',
            name='screening',
            field=models.ForeignKey(blank=True, to='activities.Screening', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jslps_screening',
            name='user_created',
            field=models.ForeignKey(related_name='activities_jslps_screening_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jslps_screening',
            name='user_modified',
            field=models.ForeignKey(related_name='activities_jslps_screening_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
