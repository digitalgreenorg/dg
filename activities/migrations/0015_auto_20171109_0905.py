# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0014_auto_20171109_0905'),
        ('people', '0008_auto_20171109_0905'),
        ('activities', '0014_auto_20170522_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSLPS_Adoption',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('member_code', models.CharField(max_length=100)),
                ('jslps_date_of_adoption', models.DateField()),
                ('jslps_date_of_entry', models.DateField()),
                ('jslps_akmcode', models.ForeignKey(to='people.JSLPS_Animator')),
                ('jslps_video', models.ForeignKey(to='videos.JSLPS_Video')),
                ('user_created', models.ForeignKey(related_name='activities_jslps_adoption_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='activities_jslps_adoption_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'JSLPS Adoption',
                'verbose_name_plural': 'JSLPS Adoption',
            },
        ),
        migrations.AlterModelOptions(
            name='jslps_screening',
            options={'verbose_name': 'JSLPS Screening', 'verbose_name_plural': 'JSLPS Screening'},
        ),
    ]
