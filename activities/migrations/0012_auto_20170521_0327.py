# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_auto_20170517_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontLineWorkerPresent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('worker_type', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='screening',
            name='frontline_worker_present',
        ),
        migrations.AddField(
            model_name='screening',
            name='worker_type',
            field=models.ManyToManyField(to='activities.FrontLineWorkerPresent', null=True),
        ),
    ]
