# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0011_auto_20170526_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='notation',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
    ]
