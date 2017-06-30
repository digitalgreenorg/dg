# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('project_name', models.CharField(help_text=b'Short Name of Project. It will be display on Analytics', unique=True, max_length=100)),
                ('project_description', models.CharField(max_length=200, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='partner',
            name='full_partner_name',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='partner_name',
            field=models.CharField(help_text=b'Short Name of Partner. It will be display on Analytics', max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='associate_partner',
            field=models.ManyToManyField(to='programs.Partner'),
        ),
        migrations.AddField(
            model_name='project',
            name='user_created',
            field=models.ForeignKey(related_name='programs_project_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='user_modified',
            field=models.ForeignKey(related_name='programs_project_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
