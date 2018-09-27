# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0022_auto_20180906_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('old_coco_id', models.BigIntegerField(null=True, editable=False)),
                ('practice_name', models.CharField(max_length=200, null=True, blank=True)),
                ('practice_category', models.ForeignKey(default=1, to='videos.Category')),
                ('practice_subcategory', models.ForeignKey(blank=True, to='videos.SubCategory', null=True)),
                ('practice_tag', models.ForeignKey(blank=True, to='videos.Tag', null=True)),
                ('user_created', models.ForeignKey(related_name='videos_library_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='videos_library_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Practice',
            },
        ),
        migrations.AlterUniqueTogether(
            name='library',
            unique_together=set([('practice_name', 'practice_category', 'practice_subcategory', 'practice_tag')]),
        ),
    ]
