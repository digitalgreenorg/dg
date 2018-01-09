# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0016_jslps_video_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0010_auto_20171129_0650'),
        ('activities', '0014_auto_20170522_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSLPS_Adoption',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('member_code', models.CharField(max_length=100)),
                ('jslps_date_of_adoption', models.DateField()),
                ('activity', models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')])),
                ('adoption', models.ForeignKey(blank=True, to='activities.PersonAdoptPractice', null=True)),
                ('jslps_akmcode', models.ForeignKey(to='people.JSLPS_Animator')),
                ('jslps_video', models.ForeignKey(to='videos.JSLPS_Video')),
                ('user_created', models.ForeignKey(related_name='activities_jslps_adoption_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_jslps_adoption_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'JSLPS Adoption',
                'verbose_name_plural': 'JSLPS Adoption',
            },
        ),
        migrations.CreateModel(
            name='JSLPS_PersonMeetingAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('activity', models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')])),
                ('person', models.ForeignKey(to='people.JSLPS_Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='jslps_screening',
            options={'verbose_name': 'JSLPS Screening', 'verbose_name_plural': 'JSLPS Screening'},
        ),
        migrations.AddField(
            model_name='jslps_screening',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')]),
        ),
        migrations.AddField(
            model_name='jslps_personmeetingattendance',
            name='screening',
            field=models.ForeignKey(to='activities.JSLPS_Screening'),
        ),
        migrations.AddField(
            model_name='jslps_personmeetingattendance',
            name='user_created',
            field=models.ForeignKey(related_name='activities_jslps_personmeetingattendance_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='jslps_personmeetingattendance',
            name='user_modified',
            field=models.ForeignKey(related_name='activities_jslps_personmeetingattendance_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='jslps_screening',
            name='farmers_attendance',
            field=models.ManyToManyField(to='people.JSLPS_Person', through='activities.JSLPS_PersonMeetingAttendance', blank=True),
        ),
    ]
