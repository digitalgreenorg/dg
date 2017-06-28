# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0013_auto_20170608_0556'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gaddidar',
            unique_together=set([('gaddidar_phone', 'gaddidar_name', 'mandi')]),
        ),
    ]
