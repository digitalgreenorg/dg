# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20170411_1429'),
        ('people', '0016_auto_20220721_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='partners',
            field=models.ManyToManyField(related_name='farmers', to='programs.Partner'),
        ),
    ]
