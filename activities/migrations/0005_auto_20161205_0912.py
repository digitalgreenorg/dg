# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20160715_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personadoptpractice',
            name='date_of_adoption',
            field=models.DateField(null=True, blank=True),
        ),
    ]
