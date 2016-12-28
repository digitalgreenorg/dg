# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20161228_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='directbeneficiaries',
            name='category',
            field=models.ForeignKey(to='videos.Category', null=True),
        ),
    ]
