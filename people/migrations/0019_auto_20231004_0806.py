# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0008_auto_20180820_0701'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0018_auto_20230214_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Household',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('household_name', models.CharField(max_length=100)),
                ('head_gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('user_created', models.ForeignKey(related_name='people_household_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='people_household_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('village', models.ForeignKey(to='geographies.Village')),
            ],
            options={
                'verbose_name': 'Person group',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='household',
            field=models.ForeignKey(blank=True, to='people.Household', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='household',
            unique_together=set([('household_name', 'village')]),
        ),
    ]
