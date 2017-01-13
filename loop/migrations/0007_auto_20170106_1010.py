# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0006_auto_20161230_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggregatorshareoutliers',
            name='loop_user',
            field=models.ForeignKey(related_name='loopuser', to='loop.LoopUser', null=True),
        ),
        migrations.AddField(
            model_name='gaddidarshareoutliers',
            name='loop_user',
            field=models.ForeignKey(related_name='loop_user', to='loop.LoopUser', null=True),
        ),
        migrations.AlterField(
            model_name='aggregatorshareoutliers',
            name='aggregator',
            field=models.ForeignKey(to='loop.LoopUser', null=True),
        ),
        migrations.AlterField(
            model_name='gaddidarshareoutliers',
            name='aggregator',
            field=models.ForeignKey(related_name='aggreagtor', to='loop.LoopUser', null=True),
        ),
    ]
