# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0004_auto_20220720_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoqualityreview',
            name='interview',
            field=models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='style_guide',
            field=models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
        migrations.AlterField(
            model_name='videoqualityreview',
            name='technical',
            field=models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2')]),
        ),
    ]
