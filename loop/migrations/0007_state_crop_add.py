# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0006_auto_20170120_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='crop_add',
            field=models.BooleanField(default=False),
        ),
    ]
