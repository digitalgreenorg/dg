# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20160708_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_modelfarmer',
            field=models.BooleanField(default=False),
        ),
    ]
