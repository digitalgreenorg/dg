# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0015_auto_20160830_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptionnonnegotiableverfication',
            name='adopted',
            field=models.BooleanField(default=False),
        ),
    ]
