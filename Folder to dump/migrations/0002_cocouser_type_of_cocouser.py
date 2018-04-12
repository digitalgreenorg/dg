# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('coco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocouser',
            name='type_of_cocouser',
            field=models.IntegerField(blank=True, choices=[(1, b'HNN'), (2, b'AGRICULTURE'), (3, b'BOTH')], null=True, validators=[django.core.validators.MaxValueValidator(3)]),
        ),
    ]
