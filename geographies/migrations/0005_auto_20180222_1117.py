# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geographies', '0004_auto_20171129_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='AP_District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('district_code', models.CharField(max_length=100)),
                ('district_name', models.CharField(max_length=100)),
                ('district', models.ForeignKey(blank=True, to='geographies.District', null=True)),
                ('user_created', models.ForeignKey(related_name='geographies_ap_district_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='geographies_ap_district_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'AP District',
                'verbose_name_plural': 'AP District',
            },
        ),
        migrations.CreateModel(
            name='AP_Habitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('habitation_code', models.CharField(max_length=100)),
                ('habitation_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'AP Habitation',
                'verbose_name_plural': 'AP Habitation',
            },
        ),
        migrations.CreateModel(
            name='AP_Mandal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('mandal_code', models.CharField(max_length=100)),
                ('mandal_name', models.CharField(max_length=100)),
                ('ap_district', models.ForeignKey(blank=True, to='geographies.AP_District', null=True)),
                ('block', models.ForeignKey(blank=True, to='geographies.Block', null=True)),
                ('user_created', models.ForeignKey(related_name='geographies_ap_mandal_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='geographies_ap_mandal_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'AP Block',
                'verbose_name_plural': 'AP Block',
            },
        ),
        migrations.CreateModel(
            name='AP_Village',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('village_code', models.CharField(max_length=100)),
                ('village_name', models.CharField(max_length=100)),
                ('ap_mandal', models.ForeignKey(blank=True, to='geographies.AP_Mandal', null=True)),
                ('user_created', models.ForeignKey(related_name='geographies_ap_village_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='geographies_ap_village_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('village', models.ForeignKey(blank=True, to='geographies.Village', null=True)),
            ],
            options={
                'verbose_name': 'AP Village',
                'verbose_name_plural': 'AP Village',
            },
        ),
        migrations.AddField(
            model_name='ap_habitation',
            name='ap_village',
            field=models.ForeignKey(blank=True, to='geographies.AP_Village', null=True),
        ),
        migrations.AddField(
            model_name='ap_habitation',
            name='user_created',
            field=models.ForeignKey(related_name='geographies_ap_habitation_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ap_habitation',
            name='user_modified',
            field=models.ForeignKey(related_name='geographies_ap_habitation_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
