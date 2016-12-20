# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20161216_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='screening',
            name='health_provider_present',
            field=models.BooleanField(default=False),
        ),
    ]
