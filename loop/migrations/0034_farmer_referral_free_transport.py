# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0033_auto_20180227_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='referral_free_transport',
            field=models.BooleanField(default=False),
        ),
    ]
