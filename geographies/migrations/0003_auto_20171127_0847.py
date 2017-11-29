# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0002_auto_20171109_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_block',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD')]),
        ),
        migrations.AddField(
            model_name='jslps_district',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD')]),
        ),
        migrations.AddField(
            model_name='jslps_village',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD')]),
        ),
    ]
