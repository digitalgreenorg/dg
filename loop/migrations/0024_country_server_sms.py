# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0023_auto_20180108_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='server_sms',
            field=models.BooleanField(default=False),
        ),
    ]
