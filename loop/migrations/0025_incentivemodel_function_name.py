# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='incentivemodel',
            name='function_name',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(0, b'BangladeshVolume0.5'), (1, b'BiharpostNov'), (2, b'BangladeshVolume1'), (3, b'DailyPay250'), (4, b'Volume0.25')]),
        ),
    ]
