# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0005_auto_20161202_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='days_count',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='state',
            name='helpline_number',
            field=models.CharField(default=b'0', max_length=14),
        ),
    ]
