# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geographies', '0001_initial'),
        ('videos', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('section', models.IntegerField()),
                ('serial', models.IntegerField()),
                ('text', models.CharField(max_length=100)),
                ('assessment', models.ForeignKey(blank=True, to='training.Assessment', null=True)),
                ('language', models.ForeignKey(blank=True, to='videos.Language', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('score', models.IntegerField()),
                ('participant', models.ForeignKey(blank=True, to='people.Animator', null=True)),
                ('question', models.ForeignKey(blank=True, to='training.Question', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75)),
                ('language', models.ForeignKey(blank=True, to='videos.Language', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('place', models.CharField(max_length=200)),
                ('assessment', models.ForeignKey(blank=True, to='training.Assessment', null=True)),
                ('language', models.ForeignKey(blank=True, to='videos.Language', null=True)),
                ('participants', models.ManyToManyField(to='people.Animator')),
                ('trainer', models.ManyToManyField(to='training.Trainer', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrainingUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('states', models.ManyToManyField(to='geographies.State')),
                ('user', models.OneToOneField(related_name='training_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='score',
            name='training',
            field=models.ForeignKey(blank=True, to='training.Training', null=True),
            preserve_default=True,
        ),
    ]
