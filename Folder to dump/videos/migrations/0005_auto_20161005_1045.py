# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_remove_video_farmers_shown'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='reviewed_by',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='reviewer',
            field=models.IntegerField(blank=True, choices=[(0, b'Digital Green'), (1, b'Partner')], null=True, verbose_name=b'Organisation', validators=[django.core.validators.MaxValueValidator(1)]),
        ),
    ]
