# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop_ivr', '0005_auto_20171215_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsStatus',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('textlocal_sms_id', models.CharField(max_length=150, null=True, blank=True)),
                ('status', models.CharField(max_length=150, null=True, blank=True)),
                ('delivery_time', models.DateTimeField(null=True, blank=True)),
                ('api_call_initiation_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='priceinfoincoming',
            name='return_result_to_app',
        ),
        migrations.AddField(
            model_name='priceinfoincoming',
            name='is_rate_available',
            field=models.IntegerField(default=1, db_index=True, choices=[(0, b'NA'), (1, b'Available'), (2, b'Partial Available')]),
        ),
        migrations.AddField(
            model_name='smsstatus',
            name='price_info_incoming',
            field=models.ForeignKey(to='loop_ivr.PriceInfoIncoming'),
        ),
        migrations.AddField(
            model_name='smsstatus',
            name='user_created',
            field=models.ForeignKey(related_name='loop_ivr_smsstatus_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='smsstatus',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_ivr_smsstatus_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
