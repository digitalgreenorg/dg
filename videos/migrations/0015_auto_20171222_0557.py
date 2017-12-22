# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_apvideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BluefrogPractice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('practice_id', models.CharField(max_length=10, null=True)),
                ('practice_method_name', models.CharField(max_length=255, null=True)),
                ('practice_method_name_telgu', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BluefrogSubcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crop_id', models.CharField(max_length=10, null=True)),
                ('crop_name', models.CharField(max_length=255, null=True)),
                ('crop_name_telgu', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DistrictScreening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('districtscreening_id', models.CharField(max_length=10, null=True)),
                ('districtscreening_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='apvideo',
            name='bluefrog_practice',
        ),
        migrations.AddField(
            model_name='apvideo',
            name='bluefrog_subcategory',
            field=models.ForeignKey(blank=True, to='videos.BluefrogSubcategory', null=True),
        ),
        migrations.AddField(
            model_name='apvideo',
            name='districtscreening',
            field=models.ManyToManyField(to='videos.DistrictScreening', blank=True),
        ),
        migrations.AddField(
            model_name='apvideo',
            name='bluefrog_practice',
            field=models.ManyToManyField(to='videos.BluefrogPractice', blank=True),
        ),
    ]
