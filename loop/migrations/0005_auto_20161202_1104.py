# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0004_auto_20160914_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gaddidar',
            name='discount_criteria',
            field=models.IntegerField(default=0, choices=[(0, b'Volume'), (1, b'Amount')]),
        ),
        migrations.AlterField(
            model_name='loopuser',
            name='role',
            field=models.IntegerField(choices=[(1, b'Admin'), (2, b'Aggregator'), (3, b'Testing')]),
        ),
    ]

