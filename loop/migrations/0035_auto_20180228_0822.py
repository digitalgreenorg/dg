# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0034_farmer_referral_free_transport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='qr_code',
            field=models.CharField(default=None, max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='farmertransportcode',
            name='qr_code',
            field=models.IntegerField(max_length=30, null=True, blank=True),
        ),
    ]
