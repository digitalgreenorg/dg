# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0013_auto_20170602_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='phone_start',
            field=models.CharField(default=789, max_length=15, null=True, blank=True),
        ),
    ]
