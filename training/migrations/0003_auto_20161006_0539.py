# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_auto_20160708_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='participant',
            field=models.ForeignKey(default=None, to='people.Animator'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='question',
            field=models.ForeignKey(default=None, to='training.Question'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='training',
            field=models.ForeignKey(default=None, to='training.Training'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('training', 'participant', 'question')]),
        ),
    ]
