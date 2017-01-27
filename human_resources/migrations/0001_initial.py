# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienceQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('hierarchy_number', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Geographies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('conclusion', models.TextField()),
                ('hierarchy_num', models.FloatField(default=0)),
                ('geography', models.ForeignKey(to='human_resources.Geography')),
            ],
            options={
                'ordering': ['-geography__hierarchy_number', 'geography__name', '-hierarchy_num', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KeyResponsibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point', models.CharField(max_length=500)),
                ('job', models.ForeignKey(to='human_resources.Job')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('designation', models.CharField(max_length=100)),
                ('personal_intro', models.TextField(help_text=b'Minimum Length Should be 250\n                                                 and Maximum 1350', validators=[django.core.validators.MaxLengthValidator(1350), django.core.validators.MinLengthValidator(250)])),
                ('team', models.CharField(max_length=100, choices=[(b'Executive Leadership Team', b'Executive Leadership Team'), (b'Technology Team', b'Technology Team'), (b'Program Team', b'Program Team'), (b'Support Team', b'Support Team')])),
                ('image', models.ImageField(help_text=b'Minimum Width Should be 100\n                                         and Minimum Height should be 100', upload_to=b'team/')),
                ('hierarchy_num', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='place',
            field=models.ForeignKey(to='human_resources.Place', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='experiencequalification',
            name='job',
            field=models.ForeignKey(to='human_resources.Job'),
            preserve_default=True,
        ),
    ]
