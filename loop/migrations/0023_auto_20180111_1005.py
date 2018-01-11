# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0022_auto_20180102_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='version',
            field=models.CharField(default=b'0', max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='smslog',
            name='model_ids',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='state',
            name='server_sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='combinedtransaction',
            name='payment_sms',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='daytransportation',
            name='payment_sms',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='smslog',
            name='sms_body',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
