# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('coco', '0002_cocouser_type_of_cocouser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocouser',
            name='type_of_cocouser',
            field=models.IntegerField(blank=True, choices=[(1, b'HNN'), (2, b'AGRICULTURE'), (3, b'BOTH'), (4, b'UPAVAN')], null=True, validators=[django.core.validators.MaxValueValidator(3)]),
        ),
    ]
