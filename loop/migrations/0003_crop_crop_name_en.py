# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0002_auto_20160817_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='crop_name_en',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
