# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0003_auto_20170810_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='type_of_subscriber',
            field=models.IntegerField(default=3, choices=[(0, b'Farmer'), (1, b'Aggregator'), (2, b'DG'), (3, b'Other')]),
        ),
    ]
