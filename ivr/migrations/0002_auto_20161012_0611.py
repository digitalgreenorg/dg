# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='audio_file',
            field=models.FileField(upload_to=b'/Users/darthvader/dgcode/dg/dg/media/social_website/uploadsivrs/'),
        ),
    ]
