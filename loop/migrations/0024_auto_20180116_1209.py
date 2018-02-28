# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0023_auto_20180111_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='helplineexpert',
            name='partner',
            field=models.ForeignKey(blank=True, to='loop.Partner', null=True),
        ),
        migrations.AddField(
            model_name='helplineexpert',
            name='state',
            field=models.ForeignKey(blank=True, to='loop.State', null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='helpline_number',
            field=models.CharField(default=b'0', max_length=14),
        ),
    ]
