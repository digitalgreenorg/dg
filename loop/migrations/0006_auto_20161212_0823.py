# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0005_auto_20161202_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gaddidarshareoutliers',
            name='gaddidar',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'mandi', to='loop.Gaddidar', chained_field=b'mandi'),
        ),
    ]
