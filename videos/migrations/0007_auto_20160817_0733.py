# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20160811_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='is_dg_video',
            field=models.BooleanField(db_index=True, verbose_name=b'Is DigitalGreen Video'),
        ),
    ]
