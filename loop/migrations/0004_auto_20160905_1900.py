# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0003_crop_crop_name_en'),
    ]

    operations = [
        migrations.CreateModel(
            name='Croplanguage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('crop_name', models.CharField(max_length=30)),
                ('crop', models.ForeignKey(to='loop.Crop')),
            ],
        ),
        migrations.CreateModel(
            name='GaddidarCommission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('start_date', models.DateField()),
                ('discount_percent', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
            ],
        ),
        migrations.CreateModel(
            name='GaddidarShareOutliers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('aggregator', models.ForeignKey(to='loop.LoopUser')),
            ],
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='discount_criteria',
            field=models.IntegerField(default=0, choices=[(1, b'Volume'), (2, b'Amount')]),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=25),
        ),
        migrations.AddField(
            model_name='gaddidarshareoutliers',
            name='gaddidar',
            field=models.ForeignKey(to='loop.Gaddidar'),
        ),
        migrations.AddField(
            model_name='gaddidarshareoutliers',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
        ),
        migrations.AddField(
            model_name='gaddidarshareoutliers',
            name='user_created',
            field=models.ForeignKey(related_name='loop_gaddidarshareoutliers_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='gaddidarshareoutliers',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_gaddidarshareoutliers_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='gaddidarcommission',
            name='gaddidar',
            field=models.ForeignKey(to='loop.Gaddidar'),
        ),
        migrations.AddField(
            model_name='gaddidarcommission',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
        ),
        migrations.AddField(
            model_name='gaddidarcommission',
            name='user_created',
            field=models.ForeignKey(related_name='loop_gaddidarcommission_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='gaddidarcommission',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_gaddidarcommission_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='croplanguage',
            name='language',
            field=models.ForeignKey(to='loop.Language', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='gaddidarshareoutliers',
            unique_together=set([('date', 'gaddidar', 'aggregator', 'mandi')]),
        ),
        migrations.AlterUniqueTogether(
            name='gaddidarcommission',
            unique_together=set([('start_date', 'gaddidar', 'mandi')]),
        ),
    ]
