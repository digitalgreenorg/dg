# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qacoco', '0019_auto_20160830_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='QAReviewerCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='qareviewername',
            name='reviewer_category',
            field=models.ForeignKey(to='qacoco.QAReviewerCategory'),
        ),
        migrations.DeleteModel(
            name='QAReviewer',
        ),
    ]
