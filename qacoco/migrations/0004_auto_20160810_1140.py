# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qacoco', '0003_auto_20160809_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='qacocouser',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='qacocouser',
            name='time_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='qacocouser',
            name='user_created',
            field=models.ForeignKey(related_name='qacoco_qacocouser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='qacocouser',
            name='user_modified',
            field=models.ForeignKey(related_name='qacoco_qacocouser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
