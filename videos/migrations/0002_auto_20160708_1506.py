# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='review_status',
            field=models.IntegerField(default=0, choices=[(0, b'Not Reviewed'), (1, b'Reviewed')], validators=[django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='video',
            name='reviewer',
            field=models.IntegerField(blank=True, choices=[(0, b'Digital Green'), (1, b'Partner')], null=True, validators=[django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.IntegerField(choices=[(1, b'Eligible for Adoption'), (2, b'Not Eligible for adoption')], validators=[django.core.validators.MaxValueValidator(1)]),
        ),
    ]
