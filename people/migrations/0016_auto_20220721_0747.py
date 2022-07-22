# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0015_auto_20220712_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animator',
            name='role',
            field=models.IntegerField(default=0, choices=[(0, b'Animator'), (1, b'MRP'), (2, b'Video Producer')]),
        ),
    ]
