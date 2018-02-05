# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0020_farmer_correct_phone_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('is_visible', models.BooleanField(default=True)),
                ('start_date', models.DateField()),
                ('user_created', models.ForeignKey(related_name='loop_partner_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_partner_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='loopuser',
            name='partner',
            field=models.ForeignKey(default=None, blank=True, to='loop.Partner', null=True),
        ),
    ]
