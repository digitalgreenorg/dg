# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0019_auto_20180410_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='apvideo',
            name='aptags',
            field=models.ManyToManyField(to='videos.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_regional_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(unique=b'True', max_length=255),
        ),
    ]
