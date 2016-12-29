# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0006_auto_20161219_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='incentiveparameter',
            name='notation_equivalent',
            field=models.CharField(default='hello', max_length=25),
            preserve_default=False,
        ),
    ]
