# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0017_auto_20170615_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='village',
            field=models.ForeignKey(default=None, to='loop.Village', null=True),
        ),
    ]
