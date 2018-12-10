# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0021_tag_is_ap_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ForeignKey(to='videos.Category', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='subcategory',
            field=models.ForeignKey(to='videos.SubCategory', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(to='videos.Tag'),
        ),
        migrations.AlterField(
            model_name='video',
            name='videopractice',
            field=models.ManyToManyField(to='videos.VideoPractice'),
        ),
    ]
