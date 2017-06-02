# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0012_language_notation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='croplanguage',
            name='crop',
            field=models.ForeignKey(related_name='crops', to='loop.Crop'),
        ),
    ]
