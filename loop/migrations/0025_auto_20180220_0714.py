# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aggregatorincentive',
            options={'verbose_name_plural': 'Aggregator Incentive'},
        ),
        migrations.AlterModelOptions(
            name='aggregatorshareoutliers',
            options={'verbose_name_plural': 'Aggregator Share Outliers'},
        ),
        migrations.AlterModelOptions(
            name='combinedtransaction',
            options={'verbose_name_plural': 'Combined Transaction'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='daytransportation',
            options={'verbose_name_plural': 'Day Transportation'},
        ),
        migrations.AlterModelOptions(
            name='gaddidarcommission',
            options={'verbose_name_plural': 'Gaddidar Commission'},
        ),
        migrations.AlterModelOptions(
            name='gaddidarshareoutliers',
            options={'verbose_name_plural': 'Gaddidar Share Outliers'},
        ),
        migrations.AlterField(
            model_name='mandi',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='mandi',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='state',
            name='crop_add',
            field=models.BooleanField(default=False, verbose_name=b'Allow Crop Addition'),
        ),
        migrations.AlterField(
            model_name='village',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='village',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
        ),
    ]
