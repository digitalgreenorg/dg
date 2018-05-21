# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='date_of_joining',
            field=models.DateField(default=None, null=True),
        ),
    ]
