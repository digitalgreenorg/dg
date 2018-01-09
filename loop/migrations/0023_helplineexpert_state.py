# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0022_auto_20180102_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='helplineexpert',
            name='state',
            field=models.ForeignKey(blank=True, to='loop.State', null=True),
        ),
    ]
