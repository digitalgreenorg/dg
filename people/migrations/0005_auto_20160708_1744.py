# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20160708_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(999)]),
        ),
    ]
