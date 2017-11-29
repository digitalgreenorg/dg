# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0018_auto_20171127_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jslps_adoption',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')]),
        ),
        migrations.AlterField(
            model_name='jslps_screening',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY')]),
        ),
    ]
