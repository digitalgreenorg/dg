# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0004_auto_20180917_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='country',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
