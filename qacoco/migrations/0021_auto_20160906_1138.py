# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0020_auto_20160901_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoqualityreview',
            name='youtubeid',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
