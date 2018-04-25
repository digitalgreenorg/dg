# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0019_auto_20171109_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='correct_phone_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
