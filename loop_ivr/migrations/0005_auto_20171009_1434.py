# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0004_auto_20170831_1559'),
    ]

    operations = [
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
    ]
