# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20160708_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.IntegerField(choices=[(1, b'Eligible for Adoption'), (2, b'Not Eligible for adoption')], validators=[django.core.validators.MaxValueValidator(2)]),
        ),
    ]
