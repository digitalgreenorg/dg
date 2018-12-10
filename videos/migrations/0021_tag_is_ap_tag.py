# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0020_auto_20180510_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='is_ap_tag',
            field=models.BooleanField(default=True),
        ),
    ]
