# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_screening_is_dg_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='personadoptpractice',
            name='listened_to_prc',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'Listened to PRC'),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='size_land',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
    ]
