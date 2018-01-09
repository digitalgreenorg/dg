# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0025_auto_20180108_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smslog',
            name='sms_body',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
