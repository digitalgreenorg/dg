# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_auto_20180228_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerqrscan',
            name='qr_code',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
