# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0026_auto_20180521_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='transaction_count',
            field=models.IntegerField(default=0),
        ),
    ]
