# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_remove_video_farmers_shown'),
        ('qacoco', '0012_auto_20160829_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adoptionverification',
            name='adopted',
        ),
        migrations.AddField(
            model_name='adoptionverification',
            name='adopt_nonnegotiable',
            field=models.ManyToManyField(to='videos.NonNegotiable', through='qacoco.AdoptionNonNegotiableVerfication'),
        ),
    ]
