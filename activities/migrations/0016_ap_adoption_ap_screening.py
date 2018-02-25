# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0018_auto_20180222_1117'),
        ('people', '0012_auto_20180222_1117'),
        ('activities', '0015_auto_20171220_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='AP_Adoption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('member_code', models.CharField(max_length=255)),
                ('member_name', models.CharField(max_length=255)),
                ('date_of_adoption', models.DateField()),
                ('adoption_type', models.CharField(max_length=100, null=True, blank=True)),
                ('adoption', models.ForeignKey(blank=True, to='activities.PersonAdoptPractice', null=True)),
                ('ap_adopt_practice', models.ForeignKey(blank=True, to='videos.APPractice', null=True)),
                ('ap_animator', models.ForeignKey(to='people.AP_Animator')),
                ('ap_video', models.ForeignKey(blank=True, to='videos.APVideo', null=True)),
                ('user_created', models.ForeignKey(related_name='activities_ap_adoption_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_ap_adoption_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Adoption',
                'verbose_name_plural': 'Adoption',
            },
        ),
        migrations.CreateModel(
            name='AP_Screening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('screening_code', models.CharField(max_length=100)),
                ('no_of_male', models.CharField(max_length=100, null=True)),
                ('no_of_female', models.CharField(max_length=100, null=True)),
                ('total_members', models.CharField(max_length=100, null=True)),
                ('screening', models.ForeignKey(blank=True, to='activities.Screening', null=True)),
                ('user_created', models.ForeignKey(related_name='activities_ap_screening_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_ap_screening_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Screening',
                'verbose_name_plural': 'Screening',
            },
        ),
    ]
