# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0017_auto_20180202_1012'),
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
        migrations.CreateModel(
            name='APVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('video_short_name', models.CharField(max_length=40)),
                ('video_short_regionalname', models.CharField(max_length=40)),
                ('practice', models.ManyToManyField(to='videos.APPractice', blank=True)),
                ('subcategory', models.ForeignKey(blank=True, to='videos.SubCategory', null=True)),
                ('user_created', models.ForeignKey(related_name='videos_apvideo_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_apvideo_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('video', models.ForeignKey(blank=True, to='videos.Video', null=True)),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Video',
            },
        ),
    ]
