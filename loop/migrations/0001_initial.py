# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('block_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CombinedTransaction',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('status', models.IntegerField()),
                ('amount', models.FloatField()),
                ('timestamp', models.CharField(max_length=25, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('country_name', models.CharField(max_length=50)),
                ('user_created', models.ForeignKey(related_name='loop_country_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_country_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('image_path', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('crop_name', models.CharField(max_length=30)),
                ('measuring_unit', models.CharField(default=b'kg', max_length=20)),
                ('user_created', models.ForeignKey(related_name='loop_crop_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_crop_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayTransportation',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('transportation_cost', models.FloatField()),
                ('farmer_share', models.FloatField(default=0.0)),
                ('other_cost', models.FloatField(default=0.0)),
                ('vrp_fees', models.FloatField(default=0.0)),
                ('comment', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('district_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('phone', models.CharField(max_length=13)),
                ('image_path', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('user_created', models.ForeignKey(related_name='loop_farmer_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmer_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gaddidar',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gaddidar_name', models.CharField(max_length=100)),
                ('gaddidar_phone', models.CharField(max_length=13)),
                ('commission', models.FloatField(default=1.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('village', models.IntegerField(null=True)),
                ('action', models.IntegerField()),
                ('entry_table', models.CharField(max_length=100)),
                ('model_id', models.IntegerField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoopUser',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'default', max_length=100)),
                ('role', models.IntegerField(choices=[(1, b'Admin'), (2, b'Aggregator')])),
                ('mode', models.IntegerField(default=1, choices=[(1, b'Direct Sell'), (2, b'Aggregate')])),
                ('phone_number', models.CharField(default=b'0', max_length=14)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mandi',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('mandi_name', models.CharField(max_length=90)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('district', models.ForeignKey(to='loop.District')),
                ('user_created', models.ForeignKey(related_name='loop_mandi_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_mandi_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('state_name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(to='loop.Country')),
                ('user_created', models.ForeignKey(related_name='loop_state_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_state_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransportationVehicle',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_number', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('transporter_name', models.CharField(max_length=90)),
                ('transporter_phone', models.CharField(max_length=13)),
                ('block', models.ForeignKey(to='loop.Block')),
                ('user_created', models.ForeignKey(related_name='loop_transporter_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_transporter_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
                ('user_created', models.ForeignKey(related_name='loop_vehicle_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_vehicle_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('village_name', models.CharField(max_length=50)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('block', models.ForeignKey(to='loop.Block')),
                ('user_created', models.ForeignKey(related_name='loop_village_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_village_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='village',
            unique_together=set([('village_name', 'block')]),
        ),
        migrations.AlterUniqueTogether(
            name='vehicle',
            unique_together=set([('vehicle_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='transporter',
            unique_together=set([('transporter_name', 'transporter_phone')]),
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='transporter',
            field=models.ForeignKey(to='loop.Transporter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='user_created',
            field=models.ForeignKey(related_name='loop_transportationvehicle_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_transportationvehicle_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='vehicle',
            field=models.ForeignKey(to='loop.Vehicle'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='transportationvehicle',
            unique_together=set([('transporter', 'vehicle', 'vehicle_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('state_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='mandi',
            unique_together=set([('mandi_name', 'district')]),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='assigned_mandis',
            field=models.ManyToManyField(related_name='assigned_mandis', to='loop.Mandi'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='assigned_villages',
            field=models.ManyToManyField(related_name='assigned_villages', to='loop.Village'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='user',
            field=models.OneToOneField(related_name='loop_user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='user_created',
            field=models.ForeignKey(related_name='loop_loopuser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_loopuser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='village',
            field=models.ForeignKey(default=None, to='loop.Village', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='user_created',
            field=models.ForeignKey(related_name='loop_gaddidar_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_gaddidar_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gaddidar',
            unique_together=set([('gaddidar_phone', 'gaddidar_name')]),
        ),
        migrations.AddField(
            model_name='farmer',
            name='village',
            field=models.ForeignKey(to='loop.Village'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='farmer',
            unique_together=set([('phone', 'name')]),
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(to='loop.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='district',
            name='user_created',
            field=models.ForeignKey(related_name='loop_district_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='district',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_district_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('district_name', 'state')]),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='transportation_vehicle',
            field=models.ForeignKey(to='loop.TransportationVehicle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='user_created',
            field=models.ForeignKey(related_name='loop_daytransportation_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_daytransportation_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='crop',
            unique_together=set([('crop_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='country',
            unique_together=set([('country_name',)]),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='crop',
            field=models.ForeignKey(to='loop.Crop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='farmer',
            field=models.ForeignKey(to='loop.Farmer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='gaddidar',
            field=models.ForeignKey(default=True, to='loop.Gaddidar', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='user_created',
            field=models.ForeignKey(related_name='loop_combinedtransaction_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_combinedtransaction_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='combinedtransaction',
            unique_together=set([('date', 'farmer', 'crop', 'mandi', 'price', 'gaddidar', 'quantity', 'timestamp')]),
        ),
        migrations.AddField(
            model_name='block',
            name='district',
            field=models.ForeignKey(to='loop.District'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='block',
            name='user_created',
            field=models.ForeignKey(related_name='loop_block_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='block',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_block_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('block_name', 'district')]),
        ),
    ]
