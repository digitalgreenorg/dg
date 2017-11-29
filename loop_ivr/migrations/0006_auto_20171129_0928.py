# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0005_priceinfoincoming_call_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='call_id',
            field=models.CharField(max_length=100, verbose_name=b'Call / Message Id', db_index=True),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='textlocal_sms_id',
            field=models.TextField(null=True, blank=True),
        ),
    ]
