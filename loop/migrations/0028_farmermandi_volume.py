# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0027_farmer_transaction_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmermandi',
            name='volume',
            field=models.FloatField(default=0.0),
        ),
    ]
