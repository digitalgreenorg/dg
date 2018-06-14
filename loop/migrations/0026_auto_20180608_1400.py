# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_auto_20180604_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loopuser',
            name='role',
            field=models.IntegerField(choices=[(1, b'Admin'), (2, b'Aggregator'), (3, b'Testing'), (4, b'Demo')]),
        ),
    ]
