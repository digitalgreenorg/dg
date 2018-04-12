# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0012_auto_20170521_0327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screening',
            name='worker_type',
        ),
        migrations.AddField(
            model_name='screening',
            name='frontlineworkerpresent',
            field=models.ManyToManyField(to='activities.FrontLineWorkerPresent', blank=True),
        ),
    ]
