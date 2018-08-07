# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_auto_20180724_0612'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
