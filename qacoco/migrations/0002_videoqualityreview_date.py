# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoqualityreview',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
