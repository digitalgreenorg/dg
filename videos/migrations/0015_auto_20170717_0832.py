# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_auto_20170629_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videopractice',
            name='videopractice_name',
            field=models.CharField(max_length=1024),
        ),
    ]
