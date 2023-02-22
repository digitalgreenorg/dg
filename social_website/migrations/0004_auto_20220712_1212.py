# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0003_auto_20160907_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='video',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
