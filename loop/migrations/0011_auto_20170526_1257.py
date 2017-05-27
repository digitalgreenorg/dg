# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0010_auto_20170515_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='phone_digit',
            field=models.CharField(default=10, max_length=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='state',
            name='phone_start',
            field=models.CharField(default=789, max_length=4, null=True, blank=True),
        ),
    ]
