# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0010_auto_20171129_0650'),
        ('activities', '0019_auto_20171129_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSLPS_PersonMeetingAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('activity', models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')])),
                ('person', models.ForeignKey(to='people.JSLPS_Person')),
                ('screening', models.ForeignKey(to='activities.JSLPS_Screening')),
                ('user_created', models.ForeignKey(related_name='activities_jslps_personmeetingattendance_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_jslps_personmeetingattendance_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='jslps_screening',
            name='farmers_attendance',
            field=models.ManyToManyField(to='people.JSLPS_Person', through='activities.JSLPS_PersonMeetingAttendance', blank=True),
        ),
    ]
