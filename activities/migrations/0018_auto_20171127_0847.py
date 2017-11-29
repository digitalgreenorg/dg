# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0017_jslps_screening_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_adoption',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD')]),
        ),
        migrations.AlterField(
            model_name='jslps_screening',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD')]),
        ),
    ]
