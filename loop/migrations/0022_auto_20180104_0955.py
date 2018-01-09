# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0021_auto_20171208_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='helplineexpert',
            name='state',
            field=models.ForeignKey(blank=True, to='loop.State', null=True),
        ),
        migrations.AlterField(
            model_name='loopuser',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name=b'Is Active'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name=b'Is Active'),
        ),
    ]
