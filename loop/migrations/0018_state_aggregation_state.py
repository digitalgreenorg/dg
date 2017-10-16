# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0017_auto_20170827_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='aggregation_state',
            field=models.BooleanField(default=True),
        ),
    ]
