# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0004_auto_20171129_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jslps_block',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
        migrations.AlterField(
            model_name='jslps_district',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
        migrations.AlterField(
            model_name='jslps_village',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
    ]
