# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0005_gaddidar_discount_criteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='gaddidarcommission',
            name='mandi',
            field=models.ForeignKey(default=1, to='loop.Mandi'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gaddidarshareoutliers',
            name='mandi',
            field=models.ForeignKey(default=2, to='loop.Mandi'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='gaddidarcommission',
            unique_together=set([('start_date', 'gaddidar', 'mandi')]),
        ),
        migrations.AlterUniqueTogether(
            name='gaddidarshareoutliers',
            unique_together=set([('date', 'gaddidar', 'aggregator', 'mandi')]),
        ),
    ]
