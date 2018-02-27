# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0032_auto_20180227_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmertransportcode',
            name='phone',
            field=models.CharField(max_length=13, null=True, blank=True),
        ),
    ]
