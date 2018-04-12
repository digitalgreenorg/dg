# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animator',
            name='assigned_villages',
            field=models.ManyToManyField(related_name='assigned_villages', through='people.AnimatorAssignedVillage', to='geographies.Village', blank=True),
        ),
        migrations.AlterField(
            model_name='jslps_animator',
            name='assigned_villages',
            field=models.ManyToManyField(related_name='jslps_assigned_villages', through='people.JSLPS_AnimatorAssignedVillage', to='geographies.JSLPS_Village', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
