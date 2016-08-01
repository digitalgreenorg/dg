# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('data_upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='upload_DateTime',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
