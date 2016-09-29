# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qacoco', '0002_auto_20160928_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='qareviewercategory',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='qareviewercategory',
            name='time_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='qareviewercategory',
            name='user_created',
            field=models.ForeignKey(related_name='qacoco_qareviewercategory_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='qareviewercategory',
            name='user_modified',
            field=models.ForeignKey(related_name='qacoco_qareviewercategory_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='qareviewername',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='qareviewername',
            name='time_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='qareviewername',
            name='user_created',
            field=models.ForeignKey(related_name='qacoco_qareviewername_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='qareviewername',
            name='user_modified',
            field=models.ForeignKey(related_name='qacoco_qareviewername_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
