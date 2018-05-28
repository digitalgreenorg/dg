# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_incentivemodel_function_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incentivemodel',
            name='function_name',
            field=models.TextField(default=None, null=True, blank=True),
        ),
    ]
