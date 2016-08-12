# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20160715_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='screening',
            name='is_dg_video',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'Is DigitalGreen Video'),
        ),
    ]
