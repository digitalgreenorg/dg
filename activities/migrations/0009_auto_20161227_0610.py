# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0008_auto_20161226_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personadoptpractice',
            name='adopt_practice',
            field=models.CharField(max_length=1, null=True, choices=[(1, b'Yes'), (2, b'No'), (3, b'Not Applicable')]),
        ),
    ]
