# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_auto_20170414_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='question',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
