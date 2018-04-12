# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0011_jslps_person_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jslps_animator',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
        migrations.AlterField(
            model_name='jslps_animatorassignedvillage',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
        migrations.AlterField(
            model_name='jslps_person',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
        migrations.AlterField(
            model_name='jslps_persongroup',
            name='activity',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'MKSP', b'MKSP'), (b'LIVELIHOOD', b'LIVELIHOOD'), (b'GOTARY', b'GOTARY'), (b'HNN', b'HNN')]),
        ),
    ]
