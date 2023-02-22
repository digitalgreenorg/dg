# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0014_auto_20220712_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(13), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='person',
            name='father_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([]),
        ),
    ]
