# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_country_server_sms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='server_sms',
        ),
        migrations.AddField(
            model_name='state',
            name='server_sms',
            field=models.BooleanField(default=False),
        ),
    ]
