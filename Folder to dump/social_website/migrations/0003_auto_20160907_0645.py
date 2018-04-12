# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0002_auto_20160708_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
