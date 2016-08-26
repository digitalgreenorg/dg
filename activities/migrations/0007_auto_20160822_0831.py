# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20160812_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='personmeetingattendance',
            name='listened_to_prc',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'Listened to PRC'),
        ),
        migrations.AlterField(
            model_name='screening',
            name='is_dg_video',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'Is this a DigitalGreen Video?'),
        ),
    ]
