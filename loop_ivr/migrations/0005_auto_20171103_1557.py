# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop_ivr', '0004_auto_20171023_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionlog',
            name='receipt_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subscriptionlog',
            name='status_code',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
    ]
