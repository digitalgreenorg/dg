# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0002_auto_20170803_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceinfoincoming',
            name='prev_info_status',
            field=models.IntegerField(default=0, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'Wrong Query'), (3, b'No Input')]),
        ),
        migrations.AddField(
            model_name='priceinfoincoming',
            name='prev_query_code',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]
