# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0028_auto_20180327_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationsms',
            name='call_state',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
