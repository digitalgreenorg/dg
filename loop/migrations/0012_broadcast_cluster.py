# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0011_remove_broadcast_cluster'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcast',
            name='cluster',
            field=models.ManyToManyField(to='loop.LoopUser', null=True, blank=True),
        ),
    ]