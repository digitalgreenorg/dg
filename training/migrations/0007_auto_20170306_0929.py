# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_auto_20170306_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletelog',
            name='table_object',
            field=models.CharField(max_length=500),
        ),
    ]
