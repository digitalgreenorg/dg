# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0001_initial'),
        ('qacoco', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serverlog',
            old_name='district',
            new_name='block',
        ),
        migrations.RemoveField(
            model_name='qacocouser',
            name='districts',
        ),
        migrations.AddField(
            model_name='qacocouser',
            name='blocks',
            field=models.ManyToManyField(to='geographies.Block'),
        ),
    ]
