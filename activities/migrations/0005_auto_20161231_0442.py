# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20161231_0442'),
        ('activities', '0004_auto_20160715_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='personadoptpractice',
            name='adopt_practice',
            field=models.CharField(max_length=1, null=True, choices=[(b'1', b'Yes'), (b'2', b'No'), (b'3', b'Not Applicable')]),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_five',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'5'),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_four',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'4'),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_one',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'1'),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_three',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'3'),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='krp_two',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'2'),
        ),
        migrations.AddField(
            model_name='personadoptpractice',
            name='parentcategory',
            field=models.ForeignKey(blank=True, to='videos.ParentCategory', null=True),
        ),
        migrations.AddField(
            model_name='personmeetingattendance',
            name='category',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='screening',
            name='health_provider_present',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='screening',
            name='parentcategory',
            field=models.ForeignKey(blank=True, to='videos.ParentCategory', null=True),
        ),
        migrations.AlterField(
            model_name='personadoptpractice',
            name='animator',
            field=models.ForeignKey(default=None, to='people.Animator'),
            preserve_default=False,
        ),
    ]
