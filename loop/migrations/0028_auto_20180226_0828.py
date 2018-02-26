# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0027_auto_20180226_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='referred_by',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
