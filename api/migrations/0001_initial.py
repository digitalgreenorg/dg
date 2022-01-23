# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('view_name', models.CharField(max_length=200)),
                ('permission_groups', models.ManyToManyField(to='auth.Group')),
            ],
        ),
    ]
