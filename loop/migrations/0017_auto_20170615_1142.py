# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0016_merge'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='adminuser',
            name='assigned_loopusers',
            field=models.ManyToManyField(related_name='assigned_loopusers', to='loop.LoopUser'),
        ),
        
    ]
