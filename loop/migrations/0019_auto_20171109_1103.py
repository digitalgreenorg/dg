# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0018_state_aggregation_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='farmer_phone_mandatory',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='phone_start',
            field=models.CharField(default=b'7,8,9', max_length=15, null=True, blank=True),
        ),
    ]
