# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='farmer_name_en',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transporter',
            name='transporter_name_en',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
