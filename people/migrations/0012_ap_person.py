# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0006_auto_20180114_0135'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0011_jslps_person_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='AP_Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('person_code', models.CharField(max_length=100)),
                ('habitation', models.ForeignKey(blank=True, to='geographies.AP_Habitation', null=True)),
                ('person', models.ForeignKey(blank=True, to='people.Person', null=True)),
                ('user_created', models.ForeignKey(related_name='people_ap_person_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='people_ap_person_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'AP Person',
                'verbose_name_plural': 'AP Person',
            },
        ),
    ]
