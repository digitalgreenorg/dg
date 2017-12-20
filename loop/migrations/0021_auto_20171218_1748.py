# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0020_farmer_correct_phone_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CTSmsLog',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sms_body', models.CharField(max_length=300, null=True, blank=True)),
                ('test_local_id', models.CharField(max_length=20, null=True, blank=True)),
                ('farmer_no', models.CharField(max_length=13, null=True, blank=True)),
                ('user_created', models.ForeignKey(related_name='loop_ctsmslog_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_ctsmslog_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='payment_sms',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='payment_sms_id',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
    ]
