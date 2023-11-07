# Generated by Django 4.2.3 on 2023-09-18 02:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratingStation',
            fields=[
                ('GenStationName', models.CharField(max_length=100, unique=True)),
                ('GenType', models.CharField(max_length=100)),
                ('InstalledCap', models.FloatField()),
                ('GenStationID', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='GridFreq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FreqMorning', models.FloatField()),
                ('FreqEvening', models.FloatField()),
                ('TimeMaxDemandMorning', models.TimeField()),
                ('TimeMaxDemandEvening', models.TimeField()),
                ('Date', models.DateField(default=datetime.date.today, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LevelStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TBDamStorage', models.FloatField()),
                ('JuralaStorage', models.FloatField()),
                ('SrisailamStorage', models.FloatField()),
                ('NSagarStorage', models.FloatField()),
                ('PulichintalaStorage', models.FloatField()),
                ('NizamSagarStorage', models.FloatField()),
                ('PochampadStorage', models.FloatField()),
                ('SingurStorage', models.FloatField()),
                ('TBDamLevel', models.FloatField()),
                ('JuralaLevel', models.FloatField()),
                ('SrisailamLevel', models.FloatField()),
                ('NSagarLevel', models.FloatField()),
                ('PulichintalaLevel', models.FloatField()),
                ('NizamSagarLevel', models.FloatField()),
                ('PochampadLevel', models.FloatField()),
                ('SingurLevel', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LevelStorageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DamID', models.IntegerField()),
                ('DamName', models.CharField(default='', max_length=30)),
                ('Level', models.FloatField(unique=True)),
                ('Date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchDrwlData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StateID', models.IntegerField()),
                ('StateName', models.CharField(default='', max_length=30)),
                ('Schedule', models.FloatField()),
                ('Drawl', models.FloatField()),
                ('Date', models.DateField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('Date', 'StateID')},
            },
        ),
        migrations.CreateModel(
            name='DemandData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GenStationID', models.IntegerField()),
                ('MorningPeak', models.FloatField()),
                ('EveningPeak', models.FloatField()),
                ('Energy', models.FloatField()),
                ('Date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'unique_together': {('Date', 'GenStationID')},
            },
        ),
        migrations.CreateModel(
            name='CentralSectorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CentralStationID', models.IntegerField()),
                ('CenStationName', models.CharField(default='', max_length=30)),
                ('Energy', models.FloatField()),
                ('Date', models.DateField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('Date', 'CentralStationID')},
            },
        ),
    ]
