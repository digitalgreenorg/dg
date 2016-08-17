# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20160817_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='is_dg_video',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'Is DigitalGreen Video'),
        ),
    ]
