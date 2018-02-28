# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0035_auto_20180228_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmertransportcode',
            name='qr_code',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
