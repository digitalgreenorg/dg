# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0007_auto_20170214_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDeleted',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('entry_table', models.CharField(max_length=100)),
                ('table_object', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='incentivemodel',
            name='description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='aggregatorincentive',
            name='model_type',
            field=models.IntegerField(choices=[(0, b'Direct'), (1, b'Tax Based'), (2, b'Slab Based'), (3, b'Daily Pay')]),
        ),
        migrations.AlterField(
            model_name='incentivemodel',
            name='calculation_method',
            field=models.TextField(),
        ),
    ]
