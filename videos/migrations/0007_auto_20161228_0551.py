# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20161210_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectBeneficiaries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direct_beneficiaries_category', models.CharField(max_length=80, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='direct_beneficiaries',
            field=models.ManyToManyField(to='videos.DirectBeneficiaries', blank=True),
        ),
    ]
