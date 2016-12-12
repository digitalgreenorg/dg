# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20161210_1243'),
        ('activities', '0004_auto_20160715_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='personmeetingattendance',
            name='category',
            field=models.CharField(max_length=1, null=True, choices=[(0, b'Pregnant Woman'), (1, b'Mother of a child up to 6 months'), (2, b'Mother of a child 6 months to 2 years'), (3, b'Mother of a child  2 to 5 years'), (4, b'Adolescent girl (10-19 years)'), (5, b'Woman of reproductive age (15-49 years)')]),
        ),
        migrations.AddField(
            model_name='screening',
            name='parentcategory',
            field=models.ForeignKey(blank=True, to='videos.ParentCategory', null=True),
        ),
    ]
