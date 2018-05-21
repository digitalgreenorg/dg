# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0025_farmer_date_of_joining'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerMandi',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_count', models.IntegerField(default=0)),
                ('farmer', models.ForeignKey(to='loop.Farmer')),
                ('mandi', models.ForeignKey(to='loop.Mandi')),
                ('user_created', models.ForeignKey(related_name='loop_farmermandi_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmermandi_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='farmermandi',
            unique_together=set([('farmer', 'mandi')]),
        ),
    ]
