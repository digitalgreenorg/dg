# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0010_auto_20170508_0407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directbeneficiaries',
            name='category',
        ),
        migrations.AddField(
            model_name='directbeneficiaries',
            name='category',
            field=models.ManyToManyField(to='videos.Category', blank=True),
        ),
    ]
