# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0017_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='APCrop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('crop_code', models.CharField(max_length=80)),
                ('crop_name', models.CharField(max_length=80)),
                ('crop_name_telgu', models.CharField(max_length=255, null=True)),
                ('subcategory', models.ForeignKey(blank=True, to='videos.SubCategory', null=True)),
                ('user_created', models.ForeignKey(related_name='videos_apcrop_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_apcrop_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Bluefrog Crop',
                'verbose_name_plural': 'Bluefrog Crop',
            },
        ),
        migrations.CreateModel(
            name='APPractice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('pest_code', models.CharField(max_length=80)),
                ('pest_name', models.CharField(max_length=80)),
                ('pest_name_telgu', models.CharField(max_length=255, null=True)),
                ('user_created', models.ForeignKey(related_name='videos_appractice_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_appractice_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Bluefrog Practice',
                'verbose_name_plural': 'Bluefrog Practice',
            },
        ),
        migrations.AlterModelOptions(
            name='apvideo',
            options={'verbose_name': 'Video', 'verbose_name_plural': 'Video'},
        ),
        migrations.RemoveField(
            model_name='apvideo',
            name='bluefrog_practice',
        ),
        migrations.RemoveField(
            model_name='apvideo',
            name='bluefrog_subcategory',
        ),
        migrations.RemoveField(
            model_name='apvideo',
            name='districtscreening',
        ),
        migrations.AddField(
            model_name='apvideo',
            name='subcategory',
            field=models.ForeignKey(blank=True, to='videos.SubCategory', null=True),
        ),
        migrations.DeleteModel(
            name='BluefrogPractice',
        ),
        migrations.DeleteModel(
            name='BluefrogSubcategory',
        ),
        migrations.DeleteModel(
            name='DistrictScreening',
        ),
        migrations.AddField(
            model_name='apvideo',
            name='practice',
            field=models.ManyToManyField(to='videos.APPractice', blank=True),
        ),
    ]
