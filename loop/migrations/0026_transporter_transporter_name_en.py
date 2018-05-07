# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_farmer_farmer_name_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='transporter',
            name='transporter_name_en',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
