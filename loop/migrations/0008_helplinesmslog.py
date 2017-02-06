# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0007_auto_20170203_1709'),
    ]

    operations = [
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
    ]
