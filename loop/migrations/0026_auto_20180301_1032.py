# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_auto_20180301_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerqrscan',
            name='timestamp',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
