# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0005_auto_20161005_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectBeneficiaries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direct_beneficiaries_category', models.CharField(max_length=80, null=True)),
                ('category', models.ForeignKey(to='videos.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('parent_category_name', models.CharField(unique=b'True', max_length=100)),
                ('user_created', models.ForeignKey(related_name='videos_parentcategory_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_parentcategory_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'ParentCategory',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, to='videos.ParentCategory', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='direct_beneficiaries',
            field=models.ManyToManyField(to='videos.DirectBeneficiaries', blank=True),
        ),
    ]
