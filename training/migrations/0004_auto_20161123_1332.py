# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('geographies', '0001_initial'),
        ('training', '0003_auto_20161006_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='district',
            field=models.ForeignKey(blank=True, to='geographies.District', null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='partner',
            field=models.ForeignKey(blank=True, to='programs.Partner', null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='trainingType',
            field=models.BooleanField(default=True),
        ),
    ]
