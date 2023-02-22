# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20170411_1429'),
        ('people', '0017_person_partners'),
    ]

    operations = [
        migrations.AddField(
            model_name='persongroup',
            name='partners',
            field=models.ManyToManyField(related_name='farmer_groups', to='programs.Partner', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='partners',
            field=models.ManyToManyField(related_name='farmers', to='programs.Partner', blank=True),
        ),
    ]
