# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0006_auto_20180330_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceinfoincoming',
            name='is_rate_available',
            field=models.IntegerField(default=3, db_index=True, choices=[(0, b'Not Available'), (1, b'Partial Available'), (2, b'Available'), (3, b'Not Applicable')]),
        ),
    ]
