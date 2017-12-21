# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0022_loopuser_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sms_body', models.CharField(max_length=300, null=True, blank=True)),
                ('test_local_id', models.CharField(max_length=20, null=True, blank=True)),
                ('farmer_no', models.CharField(max_length=13, null=True, blank=True)),
                ('user_created', models.ForeignKey(related_name='loop_smslog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_smslog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='ctsmslog',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='ctsmslog',
            name='user_modified',
        ),
        migrations.AddField(
            model_name='farmer',
            name='registration_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='farmer',
            name='registration_sms_id',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='CTSmsLog',
        ),
    ]
