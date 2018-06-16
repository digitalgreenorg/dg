# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0030_auto_20180616_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missedcall',
            name='start_time',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
