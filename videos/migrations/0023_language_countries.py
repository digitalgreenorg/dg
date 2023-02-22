# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0008_auto_20180820_0701'),
        ('videos', '0022_auto_20180917_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='countries',
            field=models.ManyToManyField(to='geographies.Country'),
        ),
    ]
