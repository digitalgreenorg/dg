# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0013_auto_20180326_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animator',
            name='role',
            field=models.IntegerField(default=0, choices=[(1, b'MRP'), (0, b'Animator'), (2, b'Video Producer')]),
        ),
    ]
