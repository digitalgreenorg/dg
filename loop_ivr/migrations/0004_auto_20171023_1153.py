# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0003_auto_20170810_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceinfoincoming',
            name='textlocal_sms_id',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='info_status',
            field=models.IntegerField(default=4, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'Wrong Query'), (3, b'No Input'), (4, b'Not Picked/Declined')]),
        ),
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='prev_info_status',
            field=models.IntegerField(default=4, db_index=True, choices=[(0, b'Pending'), (1, b'Done'), (2, b'Wrong Query'), (3, b'No Input'), (4, b'Not Picked/Declined')]),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='type_of_subscriber',
            field=models.IntegerField(default=3, choices=[(0, b'Farmer'), (1, b'Aggregator'), (2, b'DG'), (3, b'Other')]),
        ),
    ]
