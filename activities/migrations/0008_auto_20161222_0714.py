# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_screening_health_provider_present'),
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
            model_name='screening',
            name='direct_beneficiaries',
            field=models.ManyToManyField(to='activities.DirectBeneficiaries', blank=True),
        ),
    ]
