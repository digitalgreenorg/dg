# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0026_auto_20180526_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuserassignedmandi',
            name='near_mandi',
            field=models.BooleanField(default=False),
        ),
    ]
