# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='images',
            field=models.ManyToManyField(to='social_website.ImageSpec', blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='crontimestamp',
            name='last_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='partner',
            field=models.ForeignKey(to='social_website.Partner'),
        ),
        migrations.AlterField(
            model_name='resourcevideo',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
