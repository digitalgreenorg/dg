# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0006_auto_20161230_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelplineCallLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100)),
                ('from_number', models.CharField(max_length=20)),
                ('to_number', models.CharField(max_length=20)),
                ('call_type', models.IntegerField(choices=[(0, b'Incoming'), (1, b'Outgoing')])),
                ('start_time', models.DateTimeField()),
                ('user_created', models.ForeignKey(related_name='loop_helplinecalllog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_helplinecalllog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HelplineExpert',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(unique=True, max_length=20)),
                ('email_id', models.CharField(max_length=50)),
                ('expert_status', models.IntegerField(default=1, choices=[(0, b'Inactive'), (1, b'Active')])),
                ('user_created', models.ForeignKey(related_name='loop_helplineexpert_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_helplineexpert_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HelplineIncoming',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100)),
                ('from_number', models.CharField(max_length=20, db_index=True)),
                ('to_number', models.CharField(max_length=20)),
                ('incoming_time', models.DateTimeField()),
                ('last_incoming_time', models.DateTimeField()),
                ('resolved_time', models.DateTimeField(null=True, blank=True)),
                ('call_status', models.IntegerField(default=0, db_index=True, choices=[(0, b'Pending'), (1, b'Resolved'), (2, b'Declined')])),
                ('recording_url', models.CharField(max_length=200, null=True, blank=True)),
                ('acknowledge_user', models.IntegerField(default=0)),
                ('resolved_by', models.ForeignKey(blank=True, to='loop.HelplineExpert', null=True)),
                ('user_created', models.ForeignKey(related_name='loop_helplineincoming_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_helplineincoming_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HelplineOutgoing',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100)),
                ('to_number', models.CharField(max_length=20)),
                ('outgoing_time', models.DateTimeField()),
                ('from_number', models.ForeignKey(to='loop.HelplineExpert')),
                ('incoming_call', models.ForeignKey(to='loop.HelplineIncoming')),
                ('user_created', models.ForeignKey(related_name='loop_helplineoutgoing_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_helplineoutgoing_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HelplineSmsLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sms_id', models.CharField(max_length=100)),
                ('from_number', models.CharField(max_length=20)),
                ('to_number', models.CharField(max_length=20)),
                ('sms_body', models.CharField(max_length=2000, null=True, blank=True)),
                ('sent_time', models.DateTimeField()),
                ('user_created', models.ForeignKey(related_name='loop_helplinesmslog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_helplinesmslog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='helplineoutgoing',
            unique_together=set([('call_id', 'incoming_call', 'from_number', 'outgoing_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='helplineincoming',
            unique_together=set([('call_id', 'from_number', 'incoming_time')]),
        ),
    ]
