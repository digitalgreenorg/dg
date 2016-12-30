# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_auto_20161227_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personmeetingattendance',
            name='category',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
