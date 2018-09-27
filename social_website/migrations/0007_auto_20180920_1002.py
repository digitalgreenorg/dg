# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0006_auto_20180920_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='practices',
            field=models.ManyToManyField(to='videos.VideoPractice', blank=True),
        ),
    ]
