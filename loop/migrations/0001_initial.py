# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('is_visible', models.BooleanField(default=True)),
            ],
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
                ('timestamp', models.CharField(max_length=25)),
                ('is_visible', models.BooleanField(default=True)),
                ('payment_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('country_name', models.CharField(max_length=50)),
                ('is_visible', models.BooleanField(default=True)),
                ('user_created', models.ForeignKey(related_name='loop_country_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_country_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
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
                ('is_visible', models.BooleanField(default=True)),
                ('user_created', models.ForeignKey(related_name='loop_crop_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_crop_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
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
                ('is_visible', models.BooleanField(default=True)),
                ('timestamp', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('district_name', models.CharField(max_length=50)),
                ('is_visible', models.BooleanField(default=True)),
            ],
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
                ('is_visible', models.BooleanField(default=True)),
                ('user_created', models.ForeignKey(related_name='loop_farmer_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmer_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
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
                ('is_visible', models.BooleanField(default=True)),
            ],
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
            ],
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
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoopUserAssignedMandi',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('loop_user', models.ForeignKey(to='loop.LoopUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoopUserAssignedVillage',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('loop_user', models.ForeignKey(to='loop.LoopUser')),
                ('user_created', models.ForeignKey(related_name='loop_loopuserassignedvillage_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_loopuserassignedvillage_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
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
                ('is_visible', models.BooleanField(default=True)),
                ('district', models.ForeignKey(to='loop.District')),
                ('user_created', models.ForeignKey(related_name='loop_mandi_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_mandi_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('state_name', models.CharField(max_length=50)),
                ('is_visible', models.BooleanField(default=True)),
                ('country', models.ForeignKey(to='loop.Country')),
                ('user_created', models.ForeignKey(related_name='loop_state_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_state_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransportationVehicle',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_number', models.CharField(max_length=20)),
                ('is_visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('transporter_name', models.CharField(max_length=90)),
                ('transporter_phone', models.CharField(max_length=13)),
                ('is_visible', models.BooleanField(default=True)),
                ('block', models.ForeignKey(to='loop.Block')),
                ('user_created', models.ForeignKey(related_name='loop_transporter_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_transporter_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('vehicle_name', models.CharField(max_length=30)),
                ('is_visible', models.BooleanField(default=True)),
                ('user_created', models.ForeignKey(related_name='loop_vehicle_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_vehicle_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
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
                ('is_visible', models.BooleanField(default=True)),
                ('block', models.ForeignKey(to='loop.Block')),
                ('user_created', models.ForeignKey(related_name='loop_village_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_village_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='transporter',
            field=models.ForeignKey(to='loop.Transporter'),
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='user_created',
            field=models.ForeignKey(related_name='loop_transportationvehicle_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_transportationvehicle_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='transportationvehicle',
            name='vehicle',
            field=models.ForeignKey(to='loop.Vehicle'),
        ),
        migrations.AddField(
            model_name='loopuserassignedvillage',
            name='village',
            field=models.ForeignKey(to='loop.Village'),
        ),
        migrations.AddField(
            model_name='loopuserassignedmandi',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
        ),
        migrations.AddField(
            model_name='loopuserassignedmandi',
            name='user_created',
            field=models.ForeignKey(related_name='loop_loopuserassignedmandi_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='loopuserassignedmandi',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_loopuserassignedmandi_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='assigned_mandis',
            field=models.ManyToManyField(related_name='assigned_mandis', through='loop.LoopUserAssignedMandi', to='loop.Mandi', blank=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='assigned_villages',
            field=models.ManyToManyField(related_name='assigned_villages', through='loop.LoopUserAssignedVillage', to='loop.Village', blank=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='user',
            field=models.OneToOneField(related_name='loop_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='user_created',
            field=models.ForeignKey(related_name='loop_loopuser_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_loopuser_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='village',
            field=models.ForeignKey(default=None, to='loop.Village', null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='loop_user',
            field=models.ForeignKey(to='loop.LoopUser', null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='user_created',
            field=models.ForeignKey(related_name='loop_gaddidar_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_gaddidar_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='village',
            field=models.ForeignKey(to='loop.Village'),
        ),
        migrations.AddField(
            model_name='district',
            name='state',
            field=models.ForeignKey(to='loop.State'),
        ),
        migrations.AddField(
            model_name='district',
            name='user_created',
            field=models.ForeignKey(related_name='loop_district_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='district',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_district_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='transportation_vehicle',
            field=models.ForeignKey(to='loop.TransportationVehicle'),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='user_created',
            field=models.ForeignKey(related_name='loop_daytransportation_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='daytransportation',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_daytransportation_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='crop',
            field=models.ForeignKey(to='loop.Crop'),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='farmer',
            field=models.ForeignKey(to='loop.Farmer'),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='gaddidar',
            field=models.ForeignKey(default=True, to='loop.Gaddidar', null=True),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='mandi',
            field=models.ForeignKey(to='loop.Mandi'),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='user_created',
            field=models.ForeignKey(related_name='loop_combinedtransaction_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='combinedtransaction',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_combinedtransaction_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='district',
            field=models.ForeignKey(to='loop.District'),
        ),
        migrations.AddField(
            model_name='block',
            name='user_created',
            field=models.ForeignKey(related_name='loop_block_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_block_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
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
        migrations.AlterUniqueTogether(
            name='gaddidar',
            unique_together=set([('gaddidar_phone', 'gaddidar_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='farmer',
            unique_together=set([('phone', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('district_name', 'state')]),
        ),
        migrations.AlterUniqueTogether(
            name='daytransportation',
            unique_together=set([('date', 'user_created', 'timestamp')]),
        ),
        migrations.AlterUniqueTogether(
            name='crop',
            unique_together=set([('crop_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='country',
            unique_together=set([('country_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='combinedtransaction',
            unique_together=set([('date', 'user_created', 'timestamp')]),
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('block_name', 'district')]),
        ),
        migrations.AddField(
            model_name='block',
            name='block_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='crop',
            name='crop_name_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='district',
            name='district_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='gaddidar',
            name='gaddidar_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loopuser',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mandi',
            name='mandi_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='state_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='village',
            name='village_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        
        migrations.AddField(
            model_name='loopuser',
            name='preferred_language',
            field=models.ForeignKey(to='loop.Language', null=True),
        ),
    ]
