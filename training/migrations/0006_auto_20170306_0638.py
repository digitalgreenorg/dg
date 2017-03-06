# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_auto_20170227_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('entry_table', models.CharField(max_length=100)),
                ('table_object', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='logdata',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
