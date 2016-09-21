# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0021_auto_20160906_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videocontentapproval',
            name='qareviewername',
        ),
        migrations.RemoveField(
            model_name='videocontentapproval',
            name='user_created',
        ),
        migrations.RemoveField(
            model_name='videocontentapproval',
            name='user_modified',
        ),
        migrations.RemoveField(
            model_name='videocontentapproval',
            name='video',
        ),
        migrations.AlterField(
            model_name='adoptionverification',
            name='adopt_nonnegotiable',
            field=models.ManyToManyField(to='videos.NonNegotiable', through='qacoco.AdoptionNonNegotiableVerfication', blank=True),
        ),
        migrations.DeleteModel(
            name='VideoContentApproval',
        ),
    ]
